import asyncio
import json
import subprocess
import tempfile
from typing import Any, List
from pathlib import Path

from src.models.base import Model, ChatMessage, MessageRole, TokenUsage
from src.logger import logger


class ClaudeCodeModel(Model):
    """
    Model adapter for Claude Code CLI.

    Translates agent requests to Claude Code CLI commands and parses responses.
    """

    def __init__(self, model_id: str = "claude-code", **kwargs):
        super().__init__(model_id=model_id, **kwargs)
        self.working_dir = Path.cwd()

    def _format_messages_for_prompt(self, messages: List[ChatMessage]) -> str:
        """Convert ChatMessage list to a single prompt for CLI."""
        formatted = []
        for msg in messages:
            if msg.role == MessageRole.SYSTEM:
                formatted.append(f"System: {msg.content}")
            elif msg.role == MessageRole.USER:
                formatted.append(f"Human: {msg.content}")
            elif msg.role == MessageRole.ASSISTANT:
                formatted.append(f"Assistant: {msg.content}")

        return "\n\n".join(formatted)

    def _format_tools_for_claude(self, tools_to_call_from: List[Any] = None) -> str:
        """Format tool descriptions for Claude Code context."""
        if not tools_to_call_from:
            return ""

        tool_descriptions = []
        for tool in tools_to_call_from:
            tool_descriptions.append(f"- {tool.name}: {tool.description}")

        return f"\n\nAvailable tools:\n{chr(10).join(tool_descriptions)}"

    async def generate(
        self,
        messages: List[ChatMessage],
        stop_sequences: List[str] = None,
        response_format: dict = None,
        tools_to_call_from: List[Any] = None,
        **kwargs
    ) -> ChatMessage:
        """
        Generate response using Claude Code CLI.

        Strategy: Create a prompt file and invoke Claude Code programmatically.
        """
        try:
            # Format the prompt
            prompt = self._format_messages_for_prompt(messages)
            if tools_to_call_from:
                prompt += self._format_tools_for_claude(tools_to_call_from)

            # Create temporary prompt file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
                f.write(prompt)
                prompt_file = f.name

            # Prepare Claude Code command
            # Note: This assumes Claude Code can be invoked programmatically
            cmd = [
                "claude-code",  # CLI command
                "--file", prompt_file,
                "--output", "text"
            ]

            # Execute Claude Code
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.working_dir
            )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                raise RuntimeError(f"Claude Code failed: {stderr.decode()}")

            response_content = stdout.decode().strip()

            # Parse tool calls if present (simplified)
            tool_calls = self._parse_tool_calls(response_content)

            # Clean up
            Path(prompt_file).unlink(missing_ok=True)

            return ChatMessage(
                role=MessageRole.ASSISTANT,
                content=response_content,
                tool_calls=tool_calls,
                token_usage=TokenUsage(input_tokens=len(prompt.split()), output_tokens=len(response_content.split()))
            )

        except Exception as e:
            logger.error(f"Claude Code CLI error: {e}")
            raise

    def _parse_tool_calls(self, content: str) -> List[Any]:
        """Parse tool calls from Claude Code response (simplified)."""
        # This would need to be implemented based on how Claude Code formats tool calls
        # For now, return empty list
        return []


class GeminiCLIModel(Model):
    """
    Model adapter for Google Gemini CLI.

    Translates agent requests to Gemini CLI commands.
    """

    def __init__(self, model_id: str = "gemini-pro", **kwargs):
        super().__init__(model_id=model_id, **kwargs)

    def _format_for_gemini(self, messages: List[ChatMessage]) -> str:
        """Format messages for Gemini CLI."""
        # Combine all messages into a single prompt
        parts = []
        for msg in messages:
            if msg.content:
                parts.append(msg.content)
        return " ".join(parts)

    async def generate(
        self,
        messages: List[ChatMessage],
        stop_sequences: List[str] = None,
        response_format: dict = None,
        tools_to_call_from: List[Any] = None,
        **kwargs
    ) -> ChatMessage:
        """Generate response using Gemini CLI."""
        try:
            prompt = self._format_for_gemini(messages)

            # Prepare Gemini CLI command
            cmd = [
                "gemini",  # Assuming there's a gemini CLI command
                "--prompt", prompt,
                "--model", self.model_id
            ]

            # Execute Gemini CLI
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                raise RuntimeError(f"Gemini CLI failed: {stderr.decode()}")

            response_content = stdout.decode().strip()

            return ChatMessage(
                role=MessageRole.ASSISTANT,
                content=response_content,
                token_usage=TokenUsage(input_tokens=len(prompt.split()), output_tokens=len(response_content.split()))
            )

        except Exception as e:
            logger.error(f"Gemini CLI error: {e}")
            raise


class CLIBridgeModel(Model):
    """
    Advanced CLI bridge that can coordinate between multiple CLI tools.

    This approach uses a more sophisticated interaction pattern:
    1. Analyze the task type
    2. Choose appropriate CLI tool
    3. Format request appropriately
    4. Handle multi-turn conversations
    """

    def __init__(self,
                 claude_cmd: str = "claude-code",
                 gemini_cmd: str = "gemini",
                 **kwargs):
        super().__init__(model_id="cli-bridge", **kwargs)
        self.claude_cmd = claude_cmd
        self.gemini_cmd = gemini_cmd
        self.conversation_history = []

    def _select_tool(self, messages: List[ChatMessage], tools_to_call_from: List[Any] = None) -> str:
        """
        Intelligent tool selection based on task analysis.

        Claude Code: Better for file operations, code editing, web searches
        Gemini: Better for general reasoning, analysis, creative tasks
        """
        last_message = messages[-1].content.lower() if messages else ""

        # Simple heuristics (could be more sophisticated)
        if any(keyword in last_message for keyword in [
            "file", "edit", "code", "debug", "search", "web", "browser"
        ]):
            return "claude"
        elif any(keyword in last_message for keyword in [
            "analyze", "explain", "summarize", "creative", "write"
        ]):
            return "gemini"
        else:
            # Default to Claude Code for tool-heavy tasks
            return "claude" if tools_to_call_from else "gemini"

    async def generate(
        self,
        messages: List[ChatMessage],
        stop_sequences: List[str] = None,
        response_format: dict = None,
        tools_to_call_from: List[Any] = None,
        **kwargs
    ) -> ChatMessage:
        """Generate response by selecting and coordinating CLI tools."""

        selected_tool = self._select_tool(messages, tools_to_call_from)

        if selected_tool == "claude":
            model = ClaudeCodeModel()
        else:
            model = GeminiCLIModel()

        # Delegate to the selected tool
        response = await model.generate(
            messages=messages,
            stop_sequences=stop_sequences,
            response_format=response_format,
            tools_to_call_from=tools_to_call_from,
            **kwargs
        )

        # Update conversation history
        self.conversation_history.extend(messages)
        self.conversation_history.append(response)

        return response


class InteractiveCLIModel(Model):
    """
    Interactive CLI model that maintains persistent CLI sessions.

    This keeps CLI processes running and communicates through stdin/stdout
    for better performance and state management.
    """

    def __init__(self, cli_command: str, **kwargs):
        super().__init__(**kwargs)
        self.cli_command = cli_command
        self.process = None
        self.session_active = False

    async def _start_session(self):
        """Start persistent CLI session."""
        if not self.session_active:
            self.process = await asyncio.create_subprocess_exec(
                *self.cli_command.split(),
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            self.session_active = True

    async def _send_command(self, command: str) -> str:
        """Send command to CLI and get response."""
        if not self.session_active:
            await self._start_session()

        self.process.stdin.write(f"{command}\n".encode())
        await self.process.stdin.drain()

        # Read response (this would need proper protocol handling)
        response = await self.process.stdout.readline()
        return response.decode().strip()

    async def generate(
        self,
        messages: List[ChatMessage],
        **kwargs
    ) -> ChatMessage:
        """Generate using persistent CLI session."""
        prompt = self._format_messages_for_prompt(messages)
        response_content = await self._send_command(prompt)

        return ChatMessage(
            role=MessageRole.ASSISTANT,
            content=response_content,
            token_usage=TokenUsage(input_tokens=len(prompt.split()), output_tokens=len(response_content.split()))
        )

    async def close_session(self):
        """Clean up CLI session."""
        if self.session_active and self.process:
            self.process.terminate()
            await self.process.wait()
            self.session_active = False


class CLIModelFactory:
    """Factory for creating CLI model instances based on detection results"""

    @staticmethod
    def create_claude_code_cli() -> ClaudeCodeModel:
        """Create Claude Code CLI model"""
        return ClaudeCodeModel(model_id="claude-code-cli")

    @staticmethod
    def create_gemini_cli() -> GeminiCLIModel:
        """Create Gemini CLI model"""
        return GeminiCLIModel(model_id="gemini-cli")

    @classmethod
    def create_from_detection(cls, detected_tools: dict) -> dict:
        """Create CLI models based on detection results

        Args:
            detected_tools: Results from CLIToolDetector

        Returns:
            Dictionary mapping model names to CLI model instances
        """
        models = {}

        # Create Claude Code CLI models if available
        if detected_tools.get('claude_code_cli', {}).get('available', False):
            claude_model = cls.create_claude_code_cli()
            models['claude-code-cli'] = claude_model
            # Also register under API model names for easy substitution
            models['claude-3.7-sonnet-thinking'] = claude_model
            models['claude37-sonnet'] = claude_model
            logger.info("Registered Claude Code CLI models")

        # Create Gemini CLI models if available
        if detected_tools.get('gemini_cli', {}).get('available', False):
            gemini_model = cls.create_gemini_cli()
            models['gemini-cli'] = gemini_model
            # Also register under API model names for easy substitution
            models['gemini-2.5-pro'] = gemini_model
            logger.info("Registered Gemini CLI models")

        return models