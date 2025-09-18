import os
from typing import Any, Dict, List

from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv(verbose=True)

from langchain_openai import ChatOpenAI

from src.logger import logger
from src.models.api_validator import APIConfigValidator
from src.models.cli_detector import cli_detector
from src.models.cli_models import CLIModelFactory
from src.models.hfllm import InferenceClientModel
from src.models.litellm import LiteLLMModel
from src.models.openaillm import OpenAIServerModel
from src.models.restful import (
    RestfulImagenModel,
    RestfulModel,
    RestfulResponseModel,
    RestfulTranscribeModel,
    RestfulVeoFetchModel,
    RestfulVeoPridictModel,
)
from src.proxy.local_proxy import ASYNC_HTTP_CLIENT, HTTP_CLIENT
from src.utils import Singleton

custom_role_conversions = {"tool-call": "assistant", "tool-response": "user"}
PLACEHOLDER = "PLACEHOLDER"


class ModelManager(metaclass=Singleton):
    def __init__(self):
        self.registered_models: dict[str, Any] = {}
        self.validator = APIConfigValidator()
        self.validation_results = {}

    def init_models(self, use_local_proxy: bool = False):
        # PRIORITY 1: Check for CLI tools first
        logger.info("Detecting CLI tools...")
        cli_tools = cli_detector.detect_all_cli_tools()
        cli_detector.log_detection_results()

        # Register CLI models if available
        cli_models = CLIModelFactory.create_from_detection(cli_tools)
        for model_name, model_instance in cli_models.items():
            self.registered_models[model_name] = model_instance
            logger.info(f"Registered CLI model: {model_name}")

        # PRIORITY 2: Validate API configurations for fallback
        logger.info("Validating API configurations...")
        self.validation_results = self.validator.validate_all_configs()
        available_providers = self.validator.get_available_providers()

        # Register API models only if CLI equivalents are not available
        self._register_api_models_with_cli_priority(available_providers, use_local_proxy, cli_tools)

        # PRIORITY 3: Always register local models as final fallback
        self._register_fallback_models(use_local_proxy)

        # PRIORITY 4: Register model aliases for missing CLI/API models
        self._register_model_aliases(cli_tools)

        # Check if we have any models registered
        if not self.registered_models:
            logger.error("No models could be registered!")
            logger.error("CLI Setup Instructions:")
            logger.error(cli_detector.get_setup_instructions())
            logger.error("API Configuration Issues:")
            logger.error(self.validator.get_configuration_guidance())
            raise RuntimeError(
                "No models available. Please set up CLI tools or configure API keys. "
                "See logs above for detailed guidance."
            )

        logger.info(f"Successfully registered {len(self.registered_models)} models")

    def _register_api_models_with_cli_priority(self, available_providers: List[str], use_local_proxy: bool, cli_tools: Dict):
        """Register API models only if CLI equivalents are not available"""

        # Check if we need OpenAI models (not covered by CLI)
        has_claude_cli = cli_tools.get('claude_code_cli', {}).get('available', False)
        if 'openai' in available_providers and not has_claude_cli:
            self._register_openai_models(use_local_proxy=use_local_proxy)
        elif 'openai' in available_providers:
            logger.info("Skipping OpenAI models - Claude Code CLI available")
        else:
            logger.warning("Skipping OpenAI models - configuration invalid")

        # Check if we need Anthropic models (covered by Claude CLI)
        if 'anthropic' in available_providers and not has_claude_cli:
            self._register_anthropic_models(use_local_proxy=use_local_proxy)
        elif 'anthropic' in available_providers:
            logger.info("Skipping Anthropic models - Claude Code CLI available")
        else:
            logger.warning("Skipping Anthropic models - configuration invalid")

        # Check if we need Google models (covered by Gemini CLI)
        has_gemini_cli = cli_tools.get('gemini_cli', {}).get('available', False)
        if 'google' in available_providers and not has_gemini_cli:
            self._register_google_models(use_local_proxy=use_local_proxy)
        elif 'google' in available_providers:
            logger.info("Skipping Google models - Gemini CLI available")
        else:
            logger.warning("Skipping Google models - configuration invalid")

    def _register_fallback_models(self, use_local_proxy: bool):
        """Register local models and other fallbacks"""
        # Always register local HuggingFace models as fallbacks
        self._register_qwen_models(use_local_proxy=use_local_proxy)

        # Register vLLM models if available
        if 'local' in self.validator.get_available_providers():
            self._register_vllm_models(use_local_proxy=use_local_proxy)

        # Register other models that don't conflict with CLI
        self._register_langchain_models(use_local_proxy=use_local_proxy)
        self._register_deepseek_models(use_local_proxy=use_local_proxy)

    def _register_model_aliases(self, cli_tools: Dict):
        """Register model aliases to prevent KeyError for missing models"""

        # Common model mappings for fallbacks
        model_mappings = {
            # Claude models -> local fallback if CLI not available
            'claude-3.7-sonnet-thinking': 'qwen2.5-32b-instruct',
            'claude37-sonnet': 'qwen2.5-32b-instruct',
            'claude-4-sonnet': 'qwen2.5-32b-instruct',

            # Gemini models -> local fallback if CLI not available
            'gemini-2.5-pro': 'qwen2.5-14b-instruct',
            'gemini-vision': 'qwen2.5-14b-instruct',

            # GPT models -> local fallback if API not available
            'gpt-4.1': 'qwen2.5-32b-instruct',
            'gpt-4o': 'qwen2.5-32b-instruct',
            'o1': 'qwen2.5-32b-instruct',
            'o3': 'qwen2.5-32b-instruct',

            # Special models -> local fallbacks
            'o3-deep-research': 'qwen2.5-32b-instruct',
            'imagen': 'local-image-placeholder',
            'veo3-predict': 'local-video-placeholder',
            'veo3-fetch': 'local-video-placeholder',
        }

        # Check which models are missing and create aliases
        for requested_model, fallback_model in model_mappings.items():
            if requested_model not in self.registered_models:
                if fallback_model in self.registered_models:
                    # Use existing fallback model
                    self.registered_models[requested_model] = self.registered_models[fallback_model]
                    logger.info(f"Aliased '{requested_model}' -> '{fallback_model}'")
                else:
                    # Create a placeholder that will warn when used
                    self.registered_models[requested_model] = self._create_placeholder_model(requested_model, fallback_model)
                    logger.warning(f"Created placeholder for '{requested_model}' -> '{fallback_model}'")

    def _create_placeholder_model(self, requested_model: str, fallback_model: str):
        """Create a placeholder model that shows helpful error messages"""

        class PlaceholderModel:
            def __init__(self, requested: str, fallback: str):
                self.model_id = requested
                self.fallback = fallback

            def __getattr__(self, name):
                logger.error(f"Model '{self.model_id}' not available. Requested fallback '{self.fallback}' also not found.")
                logger.error("To resolve this:")
                logger.error("1. Install CLI tools: npm install -g @anthropics/claude-code")
                logger.error("2. Configure API keys in .env file")
                logger.error("3. Use local models only with appropriate configuration")
                raise RuntimeError(f"Model '{self.model_id}' not available and no fallback found")

        return PlaceholderModel(requested_model, fallback_model)

    def _check_local_api_key(self, local_api_key_name: str, remote_api_key_name: str) -> str:
        api_key = os.getenv(local_api_key_name, PLACEHOLDER)
        if api_key == PLACEHOLDER:
            logger.warning(f"Local API key {local_api_key_name} is not set, using remote API key {remote_api_key_name}")
            api_key = os.getenv(remote_api_key_name, PLACEHOLDER)
        return api_key

    def _check_local_api_base(self, local_api_base_name: str, remote_api_base_name: str) -> str:
        api_base = os.getenv(local_api_base_name, PLACEHOLDER)
        if api_base == PLACEHOLDER:
            logger.warning(f"Local API base {local_api_base_name} is not set, using remote API base {remote_api_base_name}")
            api_base = os.getenv(remote_api_base_name, PLACEHOLDER)
        return api_base

    def _register_openai_models(self, use_local_proxy: bool = False):
        # gpt-4o, gpt-4.1, o1, o3, gpt-4o-search-preview
        if use_local_proxy:
            logger.info("Using local proxy for OpenAI models")
            api_key = self._check_local_api_key(local_api_key_name="SKYWORK_API_KEY",
                                                remote_api_key_name="OPENAI_API_KEY")

            # gpt-4o
            model_name = "gpt-4o"
            model_id = "openai/gpt-4o"
            client = AsyncOpenAI(
                api_key=api_key,
                base_url=self._check_local_api_base(local_api_base_name="SKYWORK_AZURE_US_API_BASE",
                                                    remote_api_base_name="OPENAI_API_BASE"),
                http_client=ASYNC_HTTP_CLIENT,
            )
            model = LiteLLMModel(
                model_id=model_id,
                http_client=client,
                custom_role_conversions=custom_role_conversions,
            )
            self.registered_models[model_name] = model

            # gpt-4.1
            model_name = "gpt-4.1"
            model_id = "openai/gpt-4.1"
            client = AsyncOpenAI(
                api_key=api_key,
                base_url=self._check_local_api_base(local_api_base_name="SKYWORK_AZURE_US_API_BASE",
                                                    remote_api_base_name="OPENAI_API_BASE"),
                http_client=ASYNC_HTTP_CLIENT,
            )
            model = LiteLLMModel(
                model_id=model_id,
                http_client=client,
                custom_role_conversions=custom_role_conversions,
            )
            self.registered_models[model_name] = model

            # o1
            model_name = "o1"
            model_id = "openai/o1"
            client = AsyncOpenAI(
                api_key=api_key,
                base_url=self._check_local_api_base(local_api_base_name="SKYWORK_AZURE_US_API_BASE",
                                                    remote_api_base_name="OPENAI_API_BASE"),
                http_client=ASYNC_HTTP_CLIENT,
            )
            model = LiteLLMModel(
                model_id=model_id,
                http_client=client,
                custom_role_conversions=custom_role_conversions,
            )
            self.registered_models[model_name] = model

            # o3
            model_name = "o3"
            model_id = "openai/o3"

            model = RestfulModel(
                api_base=self._check_local_api_base(local_api_base_name="SKYWORK_AZURE_US_API_BASE",
                                                    remote_api_base_name="OPENAI_API_BASE"),
                api_type="chat/completions",
                api_key=api_key,
                model_id=model_id,
                http_client=HTTP_CLIENT,
                custom_role_conversions=custom_role_conversions,
            )
            self.registered_models[model_name] = model

            # gpt-4o-search-preview
            model_name = "gpt-4o-search-preview"
            model_id = "gpt-4o-search-preview"
            client = AsyncOpenAI(
                api_key=api_key,
                base_url=self._check_local_api_base(local_api_base_name="SKYWORK_OPENROUTER_US_API_BASE",
                                                    remote_api_base_name="OPENAI_API_BASE"),
                http_client=ASYNC_HTTP_CLIENT,
            )
            model = LiteLLMModel(
                model_id=model_id,
                http_client=client,
                custom_role_conversions=custom_role_conversions,
            )
            self.registered_models[model_name] = model

            # wisper
            model_name = "whisper"
            model_id = "whisper"
            model = RestfulTranscribeModel(
                api_base=self._check_local_api_base(local_api_base_name="SKYWORK_AZURE_BJ_API_BASE",
                                                    remote_api_base_name="OPENAI_API_BASE"),
                api_key=api_key,
                api_type="whisper",
                model_id=model_id,
                http_client=HTTP_CLIENT,
                custom_role_conversions=custom_role_conversions,
            )
            self.registered_models[model_name] = model

            # deep research
            model_name = "o3-deep-research"
            model_id = "o3-deep-research"

            model = RestfulResponseModel(
                api_base=self._check_local_api_base(local_api_base_name="SKYWORK_SHUBIAOBIAO_API_BASE",
                                                    remote_api_base_name="OPENAI_API_BASE"),
                api_key=api_key,
                api_type="responses",
                model_id=model_id,
                http_client=HTTP_CLIENT,
                custom_role_conversions=custom_role_conversions,
            )
            self.registered_models[model_name] = model

            # gpt-5
            model_name = "gpt-5"
            model_id = "openai/gpt-5"
            client = AsyncOpenAI(
                api_key=api_key,
                base_url=self._check_local_api_base(local_api_base_name="SKYWORK_AZURE_US_API_BASE",
                                                    remote_api_base_name="OPENAI_API_BASE"),
                http_client=ASYNC_HTTP_CLIENT,
            )
            model = LiteLLMModel(
                model_id=model_id,
                http_client=client,
                custom_role_conversions=custom_role_conversions,
            )
            self.registered_models[model_name] = model

        else:
            logger.info("Using remote API for OpenAI models")
            api_key = self._check_local_api_key(local_api_key_name="OPENAI_API_KEY",
                                                remote_api_key_name="OPENAI_API_KEY")
            api_base = self._check_local_api_base(local_api_base_name="OPENAI_API_BASE",
                                                    remote_api_base_name="OPENAI_API_BASE")

            models = [
                {
                    "model_name": "gpt-4o",
                    "model_id": "gpt-4o",
                },
                {
                    "model_name": "gpt-4.1",
                    "model_id": "gpt-4.1",
                },
                {
                    "model_name": "o1",
                    "model_id": "o1",
                },
                {
                    "model_name": "o3",
                    "model_id": "o3",
                },
                {
                    "model_name": "gpt-4o-search-preview",
                    "model_id": "gpt-4o-search-preview",
                },
            ]

            for model in models:
                model_name = model["model_name"]
                model_id = model["model_id"]
                model = LiteLLMModel(
                    model_id=model_id,
                    api_key=api_key,
                    api_base=api_base,
                    custom_role_conversions=custom_role_conversions,
                )
                self.registered_models[model_name] = model


    def _register_anthropic_models(self, use_local_proxy: bool = False):
        # claude37-sonnet, claude37-sonnet-thinking
        if use_local_proxy:
            logger.info("Using local proxy for Anthropic models")
            api_key = self._check_local_api_key(local_api_key_name="SKYWORK_API_KEY",
                                                remote_api_key_name="ANTHROPIC_API_KEY")

            # claude37-sonnet
            model_name = "claude37-sonnet"
            model_id = "claude37-sonnet"
            client = AsyncOpenAI(
                api_key=api_key,
                base_url=self._check_local_api_base(local_api_base_name="SKYWORK_OPENROUTER_US_API_BASE",
                                                    remote_api_base_name="ANTHROPIC_API_BASE"),
                http_client=ASYNC_HTTP_CLIENT,
            )
            model = OpenAIServerModel(
                model_id=model_id,
                http_client=client,
                custom_role_conversions=custom_role_conversions,
            )
            self.registered_models[model_name] = model

            # claude37-sonnet-thinking
            model_name = "claude-3.7-sonnet-thinking"
            model_id = "claude-3.7-sonnet-thinking"
            client = AsyncOpenAI(
                api_key=api_key,
                base_url=self._check_local_api_base(local_api_base_name="SKYWORK_OPENROUTER_US_API_BASE",
                                                    remote_api_base_name="ANTHROPIC_API_BASE"),
                http_client=ASYNC_HTTP_CLIENT,
            )
            model = OpenAIServerModel(
                model_id=model_id,
                http_client=client,
                custom_role_conversions=custom_role_conversions,
            )
            self.registered_models[model_name] = model

            # claude-4-sonnet
            model_name = "claude-4-sonnet"
            model_id = "claude-4-sonnet"
            client = AsyncOpenAI(
                api_key=api_key,
                base_url=self._check_local_api_base(local_api_base_name="SKYWORK_OPENROUTER_US_API_BASE",
                                                    remote_api_base_name="ANTHROPIC_API_BASE"),
                http_client=ASYNC_HTTP_CLIENT,
            )
            model = OpenAIServerModel(
                model_id=model_id,
                http_client=client,
                custom_role_conversions=custom_role_conversions,
            )
            self.registered_models[model_name] = model

        else:
            logger.info("Using remote API for Anthropic models")
            api_key = self._check_local_api_key(local_api_key_name="ANTHROPIC_API_KEY",
                                                remote_api_key_name="ANTHROPIC_API_KEY")
            api_base = self._check_local_api_base(local_api_base_name="ANTHROPIC_API_BASE",
                                                    remote_api_base_name="ANTHROPIC_API_BASE")

            models = [
                {
                    "model_name": "claude37-sonnet",
                    "model_id": "claude-3-7-sonnet-20250219",
                },
                {
                    "model_name": "claude37-sonnet-thinking",
                    "model_id": "claude-3-7-sonnet-20250219",
                },
            ]

            for model in models:
                model_name = model["model_name"]
                model_id = model["model_id"]
                model = LiteLLMModel(
                    model_id=model_id,
                    api_key=api_key,
                    api_base=api_base,
                    custom_role_conversions=custom_role_conversions,
                )
                self.registered_models[model_name] = model

    def _register_google_models(self, use_local_proxy: bool = False):
        if use_local_proxy:
            logger.info("Using local proxy for Google models")
            api_key = self._check_local_api_key(local_api_key_name="SKYWORK_API_KEY",
                                                remote_api_key_name="GOOGLE_API_KEY")

            # gemini-2.5-pro
            model_name = "gemini-2.5-pro"
            model_id = "gemini-2.5-pro-preview-06-05"
            client = AsyncOpenAI(
                api_key=api_key,
                base_url=self._check_local_api_base(local_api_base_name="SKYWORK_OPENROUTER_BJ_API_BASE",
                                                    remote_api_base_name="GOOGLE_API_BASE"),
                http_client=ASYNC_HTTP_CLIENT,
            )
            model = OpenAIServerModel(
                model_id=model_id,
                http_client=client,
                custom_role_conversions=custom_role_conversions,
            )
            self.registered_models[model_name] = model

            # imagen
            model_name = "imagen"
            model_id = "imagen-3.0-generate-001"
            model = RestfulImagenModel(
                api_base=self._check_local_api_base(local_api_base_name="SKYWORK_GOOGLE_API_BASE",
                                                    remote_api_base_name="GOOGLE_API_BASE"),
                api_key=api_key,
                api_type="imagen",
                model_id=model_id,
                http_client=HTTP_CLIENT,
                custom_role_conversions=custom_role_conversions,
            )
            self.registered_models[model_name] = model

            # veo3
            model_name = "veo3-predict"
            model_id = "veo-3.0-generate-preview"
            model = RestfulVeoPridictModel(
                api_base=self._check_local_api_base(local_api_base_name="SKYWORK_GOOGLE_API_BASE",
                                                    remote_api_base_name="GOOGLE_API_BASE"),
                api_key=api_key,
                api_type="veo/predict",
                model_id=model_id,
                http_client=HTTP_CLIENT,
                custom_role_conversions=custom_role_conversions,
            )
            self.registered_models[model_name] = model

            model_name = "veo3-fetch"
            model_id = "veo-3.0-generate-preview"
            model = RestfulVeoFetchModel(
                api_base=self._check_local_api_base(local_api_base_name="SKYWORK_GOOGLE_API_BASE",
                                                    remote_api_base_name="GOOGLE_API_BASE"),
                api_key=api_key,
                api_type="veo/fetch",
                model_id=model_id,
                http_client=HTTP_CLIENT,
                custom_role_conversions=custom_role_conversions,
            )
            self.registered_models[model_name] = model


        else:
            logger.info("Using remote API for Google models")
            api_key = self._check_local_api_key(local_api_key_name="GOOGLE_API_KEY",
                                                remote_api_key_name="GOOGLE_API_KEY")
            api_base = self._check_local_api_base(local_api_base_name="GOOGLE_API_BASE",
                                                    remote_api_base_name="GOOGLE_API_BASE")

            models = [
                {
                    "model_name": "gemini-2.5-pro",
                    "model_id": "gemini-2.5-pro-preview-06-05",
                },
            ]

            for model in models:
                model_name = model["model_name"]
                model_id = model["model_id"]
                model = LiteLLMModel(
                    model_id=model_id,
                    api_key=api_key,
                    # api_base=api_base,
                    custom_role_conversions=custom_role_conversions,
                )
                self.registered_models[model_name] = model

    def _register_qwen_models(self, use_local_proxy: bool = False):
        # qwen2.5-7b-instruct
        models = [
            {
                "model_name": "qwen2.5-7b-instruct",
                "model_id": "Qwen/Qwen2.5-7B-Instruct",
            },
            {
                "model_name": "qwen2.5-14b-instruct",
                "model_id": "Qwen/Qwen2.5-14B-Instruct",
            },
            {
                "model_name": "qwen2.5-32b-instruct",
                "model_id": "Qwen/Qwen2.5-32B-Instruct",
            },
        ]
        for model in models:
            model_name = model["model_name"]
            model_id = model["model_id"]

            model = InferenceClientModel(
                model_id=model_id,
                custom_role_conversions=custom_role_conversions,
                timeout=300,  # Increase timeout to 5 minutes
                max_tokens=4096,  # Set reasonable token limit
                temperature=0.1,  # Lower temperature for more consistent tool calls
            )
            self.registered_models[model_name] = model

    def _register_langchain_models(self, use_local_proxy: bool = False):
        # langchain models
        models = [
            {
                "model_name": "langchain-gpt-4o",
                "model_id": "gpt-4o",
            },
            {
                "model_name": "langchain-gpt-4.1",
                "model_id": "gpt-4.1",
            },
            {
                "model_name": "langchain-o3",
                "model_id": "o3",
            },
        ]

        if use_local_proxy:
            logger.info("Using local proxy for LangChain models")
            api_key = self._check_local_api_key(local_api_key_name="SKYWORK_API_KEY",
                                                remote_api_key_name="OPENAI_API_KEY")
            api_base = self._check_local_api_base(local_api_base_name="SKYWORK_API_BASE",
                                                    remote_api_base_name="OPENAI_API_BASE")

            for model in models:
                model_name = model["model_name"]
                model_id = model["model_id"]

                model = ChatOpenAI(
                    model=model_id,
                    api_key=api_key,
                    base_url=api_base,
                    http_client=HTTP_CLIENT,
                    http_async_client=ASYNC_HTTP_CLIENT,
                )
                self.registered_models[model_name] = model

        else:
            logger.info("Using remote API for LangChain models")
            api_key = self._check_local_api_key(local_api_key_name="OPENAI_API_KEY",
                                                remote_api_key_name="OPENAI_API_KEY")
            api_base = self._check_local_api_base(local_api_base_name="OPENAI_API_BASE",
                                                    remote_api_base_name="OPENAI_API_BASE")

            for model in models:
                model_name = model["model_name"]
                model_id = model["model_id"]

                model = ChatOpenAI(
                    model=model_id,
                    api_key=api_key,
                    base_url=api_base,
                )
                self.registered_models[model_name] = model
    def _register_vllm_models(self, use_local_proxy: bool = False):
        # qwen
        api_key = self._check_local_api_key(local_api_key_name="QWEN_API_KEY",
                                                remote_api_key_name="QWEN_API_KEY")
        api_base = self._check_local_api_base(local_api_base_name="QWEN_API_BASE",
                                                    remote_api_base_name="QWEN_API_BASE")
        models = [
            {
                "model_name": "Qwen",
                "model_id": "Qwen",
            }
        ]
        for model in models:
            model_name = model["model_name"]
            model_id = model["model_id"]

            client = AsyncOpenAI(
                api_key=api_key,
                base_url=api_base,
            )
            model = OpenAIServerModel(
                model_id=model_id,
                http_client=client,
                custom_role_conversions=custom_role_conversions,
            )
            self.registered_models[model_name] = model

        # Qwen-VL
        api_key_VL = self._check_local_api_key(local_api_key_name="QWEN_VL_API_KEY",
                                                remote_api_key_name="QWEN_VL_API_KEY")
        api_base_VL = self._check_local_api_base(local_api_base_name="QWEN_VL_API_BASE",
                                                    remote_api_base_name="QWEN_VL_API_BASE")
        models = [
            {
                "model_name": "Qwen-VL",
                "model_id": "Qwen-VL",
            }
        ]
        for model in models:
            model_name = model["model_name"]
            model_id = model["model_id"]

            client = AsyncOpenAI(
                api_key=api_key_VL,
                base_url=api_base_VL,
            )
            model = OpenAIServerModel(
                model_id=model_id,
                http_client=client,
                custom_role_conversions=custom_role_conversions,
            )
            self.registered_models[model_name] = model

    def _register_deepseek_models(self, use_local_proxy: bool = False):
        # deepseek models
        if use_local_proxy:
            # deepseek-chat
            logger.info("Using local proxy for DeepSeek models")
            api_key = self._check_local_api_key(local_api_key_name="SKYWORK_API_KEY",
                                                remote_api_key_name="SKYWORK_API_KEY")
            api_base = self._check_local_api_base(local_api_base_name="SKYWORK_DEEPSEEK_API_BASE",
                                                  remote_api_base_name="SKYWORK_API_BASE")

            model_name = "deepseek-chat"
            model_id = "deepseek-chat"
            client = AsyncOpenAI(
                api_key=api_key,
                base_url=api_base,
                http_client=ASYNC_HTTP_CLIENT,
            )
            model = OpenAIServerModel(
                model_id=model_id,
                http_client=client,
                custom_role_conversions=custom_role_conversions,
            )
            self.registered_models[model_name] = model

            # deepseek-reasoner
            api_key = self._check_local_api_key(local_api_key_name="SKYWORK_API_KEY",
                                                remote_api_key_name="SKYWORK_API_KEY")
            api_base = self._check_local_api_base(local_api_base_name="SKYWORK_DEEPSEEK_API_BASE",
                                                    remote_api_base_name="SKYWORK_API_BASE")

            model_name = "deepseek-reasoner"
            model_id = "deepseek-reasoner"
            client = AsyncOpenAI(
                api_key=api_key,
                base_url=api_base,
                http_client=ASYNC_HTTP_CLIENT,
            )
            model = OpenAIServerModel(
                model_id=model_id,
                http_client=client,
                custom_role_conversions=custom_role_conversions,
            )
            self.registered_models[model_name] = model
        else:
            logger.warning("DeepSeek models are not supported in remote API mode.")
