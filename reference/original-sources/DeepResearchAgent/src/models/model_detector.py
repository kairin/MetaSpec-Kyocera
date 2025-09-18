"""
Model availability detector and user selection interface.

This module detects available model backends and provides a TUI for user selection.
"""

import asyncio
import os
import shutil
import subprocess
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.text import Text


class ModelBackend(Enum):
    """Available model backend types."""
    API_OPENAI = "api_openai"
    API_ANTHROPIC = "api_anthropic"
    API_GOOGLE = "api_google"
    CLI_CLAUDE_CODE = "cli_claude_code"
    CLI_GEMINI = "cli_gemini"
    LOCAL_VLLM = "local_vllm"
    LOCAL_TRANSFORMERS = "local_transformers"


@dataclass
class ModelOption:
    """Model option with availability and configuration."""
    backend: ModelBackend
    name: str
    description: str
    available: bool
    priority: int  # Lower = higher priority
    requirements: List[str]
    model_id: str
    config_template: dict


class ModelDetector:
    """Detects available model backends and their capabilities."""

    def __init__(self):
        self.console = Console()

    def check_api_key(self, env_var: str) -> bool:
        """Check if API key is set and not placeholder."""
        key = os.getenv(env_var, "").strip()
        return bool(key) and key not in ["", "xxxxxx", "your_key_here", "none"]

    def check_cli_command(self, command: str) -> bool:
        """Check if CLI command is available."""
        return shutil.which(command) is not None

    async def check_claude_code(self) -> Tuple[bool, str]:
        """Check Claude Code CLI availability and version."""
        try:
            # Try multiple possible commands
            commands_to_try = ["claude-code", "claude", "claude_code"]

            for cmd in commands_to_try:
                if shutil.which(cmd):
                    # Try to get version
                    result = subprocess.run([cmd, "--version"],
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        return True, f"Found {cmd}: {result.stdout.strip()}"

            return False, "Claude Code CLI not found"
        except Exception as e:
            return False, f"Error checking Claude Code: {e}"

    async def check_gemini_cli(self) -> Tuple[bool, str]:
        """Check Google Gemini CLI availability."""
        try:
            # Try multiple possible commands
            commands_to_try = ["gemini", "gcloud", "google-generativeai"]

            for cmd in commands_to_try:
                if shutil.which(cmd):
                    if cmd == "gcloud":
                        # Check if AI Platform is enabled
                        result = subprocess.run(["gcloud", "ai", "--help"],
                                              capture_output=True, text=True, timeout=10)
                        if result.returncode == 0:
                            return True, f"Found gcloud with AI Platform"
                    else:
                        result = subprocess.run([cmd, "--version"],
                                              capture_output=True, text=True, timeout=10)
                        if result.returncode == 0:
                            return True, f"Found {cmd}: {result.stdout.strip()}"

            return False, "Gemini CLI not found"
        except Exception as e:
            return False, f"Error checking Gemini CLI: {e}"

    def check_local_gpu(self) -> bool:
        """Check if GPU is available for local models."""
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False

    def check_local_dependencies(self, backend: ModelBackend) -> bool:
        """Check if local model dependencies are installed."""
        if backend == ModelBackend.LOCAL_VLLM:
            try:
                import vllm
                return True
            except ImportError:
                return False
        elif backend == ModelBackend.LOCAL_TRANSFORMERS:
            try:
                import transformers
                import torch
                return True
            except ImportError:
                return False
        return False

    async def detect_available_models(self) -> List[ModelOption]:
        """Detect all available model options."""
        options = []

        # API-based models
        if self.check_api_key("OPENAI_API_KEY"):
            options.append(ModelOption(
                backend=ModelBackend.API_OPENAI,
                name="OpenAI GPT-4",
                description="GPT-4 via OpenAI API (requires API key)",
                available=True,
                priority=1,
                requirements=["OPENAI_API_KEY"],
                model_id="gpt-4.1",
                config_template={"type": "openai", "model_id": "gpt-4.1"}
            ))

        if self.check_api_key("ANTHROPIC_API_KEY"):
            options.append(ModelOption(
                backend=ModelBackend.API_ANTHROPIC,
                name="Claude 3.7 Sonnet",
                description="Claude via Anthropic API (requires API key)",
                available=True,
                priority=1,
                requirements=["ANTHROPIC_API_KEY"],
                model_id="claude-3.7-sonnet",
                config_template={"type": "anthropic", "model_id": "claude-3.7-sonnet"}
            ))

        if self.check_api_key("GOOGLE_API_KEY"):
            options.append(ModelOption(
                backend=ModelBackend.API_GOOGLE,
                name="Gemini 2.5 Pro",
                description="Gemini via Google API (requires API key)",
                available=True,
                priority=1,
                requirements=["GOOGLE_API_KEY"],
                model_id="gemini-2.5-pro",
                config_template={"type": "google", "model_id": "gemini-2.5-pro"}
            ))

        # CLI-based models
        claude_available, claude_info = await self.check_claude_code()
        options.append(ModelOption(
            backend=ModelBackend.CLI_CLAUDE_CODE,
            name="Claude Code CLI",
            description=f"Claude via local CLI tool - {claude_info}",
            available=claude_available,
            priority=2,  # Preferred over APIs for code tasks
            requirements=["claude-code CLI"],
            model_id="claude-code",
            config_template={"type": "cli_claude", "command": "claude-code"}
        ))

        gemini_available, gemini_info = await self.check_gemini_cli()
        options.append(ModelOption(
            backend=ModelBackend.CLI_GEMINI,
            name="Gemini CLI",
            description=f"Gemini via local CLI tool - {gemini_info}",
            available=gemini_available,
            priority=2,
            requirements=["gemini CLI or gcloud"],
            model_id="gemini-cli",
            config_template={"type": "cli_gemini", "command": "gemini"}
        ))

        # Local models
        has_gpu = self.check_local_gpu()
        if self.check_local_dependencies(ModelBackend.LOCAL_VLLM):
            options.append(ModelOption(
                backend=ModelBackend.LOCAL_VLLM,
                name="Local vLLM",
                description=f"Local models via vLLM {'(GPU)' if has_gpu else '(CPU)'}",
                available=True,
                priority=3,
                requirements=["vLLM", "GPU recommended"],
                model_id="qwen2.5-32b-instruct",
                config_template={"type": "vllm", "model_id": "qwen2.5-32b-instruct"}
            ))

        if self.check_local_dependencies(ModelBackend.LOCAL_TRANSFORMERS):
            options.append(ModelOption(
                backend=ModelBackend.LOCAL_TRANSFORMERS,
                name="Local Transformers",
                description=f"Local models via Transformers {'(GPU)' if has_gpu else '(CPU)'}",
                available=True,
                priority=4,
                requirements=["transformers", "torch"],
                model_id="qwen2.5-7b-instruct",
                config_template={"type": "transformers", "model_id": "qwen2.5-7b-instruct"}
            ))

        # Sort by priority (available first, then by priority number)
        options.sort(key=lambda x: (not x.available, x.priority))
        return options

    def display_model_options(self, options: List[ModelOption]) -> None:
        """Display available model options in a nice table."""
        table = Table(title="🤖 Available Model Backends", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=3)
        table.add_column("Name", style="bold")
        table.add_column("Description")
        table.add_column("Status", justify="center")
        table.add_column("Requirements", style="dim")

        for i, option in enumerate(options, 1):
            status = "✅ Available" if option.available else "❌ Not Available"
            status_style = "green" if option.available else "red"

            requirements_text = ", ".join(option.requirements)

            table.add_row(
                str(i),
                option.name,
                option.description,
                Text(status, style=status_style),
                requirements_text
            )

        self.console.print(table)

    def get_user_selection(self, options: List[ModelOption]) -> Optional[ModelOption]:
        """Get user's model selection via TUI."""
        available_options = [opt for opt in options if opt.available]

        if not available_options:
            self.console.print("❌ No model backends are available!", style="bold red")
            self.console.print("\nTo use this system, you need at least one of:")
            self.console.print("• API keys for OpenAI, Anthropic, or Google")
            self.console.print("• Claude Code CLI installed")
            self.console.print("• Gemini CLI or gcloud installed")
            self.console.print("• Local model dependencies (vLLM or Transformers)")
            return None

        self.console.print("\n🎯 Select your preferred model backend:")

        # Show recommended option
        recommended = available_options[0]
        self.console.print(f"\n💡 Recommended: {recommended.name}", style="bold green")

        # Get user choice
        choices = [str(i) for i in range(1, len(options) + 1) if options[i-1].available]
        choice = Prompt.ask(
            "Enter model ID",
            choices=choices,
            default="1" if available_options else None,
            show_choices=True
        )

        if choice:
            selected_index = int(choice) - 1
            return options[selected_index]

        return None

    async def interactive_model_selection(self) -> Optional[Dict]:
        """Interactive model selection TUI."""
        self.console.print("\n" + "="*60)
        self.console.print("🚀 DeepResearchAgent Model Configuration", style="bold blue", justify="center")
        self.console.print("="*60)

        # Detect available models
        self.console.print("\n🔍 Detecting available model backends...")
        options = await self.detect_available_models()

        # Display options
        self.display_model_options(options)

        # Get user selection
        selected = self.get_user_selection(options)

        if not selected:
            return None

        self.console.print(f"\n✅ Selected: {selected.name}", style="bold green")

        # Ask for confirmation and any additional configuration
        if Confirm.ask(f"Proceed with {selected.name}?", default=True):
            return self._build_model_config(selected)

        return None

    def _build_model_config(self, option: ModelOption) -> Dict:
        """Build configuration for selected model."""
        base_config = {
            "backend": option.backend.value,
            "model_id": option.model_id,
            "name": option.name,
            **option.config_template
        }

        # Add backend-specific configuration
        if option.backend == ModelBackend.CLI_CLAUDE_CODE:
            base_config.update({
                "command": "claude-code",
                "timeout": 300,
                "working_dir": os.getcwd()
            })
        elif option.backend == ModelBackend.CLI_GEMINI:
            base_config.update({
                "command": "gemini",
                "timeout": 180,
                "model": "gemini-pro"
            })

        return base_config


async def main():
    """Example usage of the model detector."""
    detector = ModelDetector()
    config = await detector.interactive_model_selection()

    if config:
        print("\n🎉 Configuration generated:")
        print(config)
    else:
        print("\n❌ No configuration selected")


if __name__ == "__main__":
    asyncio.run(main())