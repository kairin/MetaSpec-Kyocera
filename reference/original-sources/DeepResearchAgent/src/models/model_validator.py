"""Dynamic model validation system for TUI display."""

import os
from typing import Dict, List, Tuple
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from src.models.cli_detector import CLIToolDetector


class ModelValidator:
    """Validates and displays available models for user."""

    def __init__(self):
        self.console = Console()
        self.cli_detector = CLIToolDetector()

    def validate_all_models(self) -> Dict[str, any]:
        """Validate all available model connections."""
        results = {
            'claude_cli': self._validate_claude_cli(),
            'gemini_cli': self._validate_gemini_cli(),
            'huggingface': self._validate_huggingface(),
            'summary': {}
        }

        # Generate summary
        working_models = []
        connection_methods = []

        if results['claude_cli']['available']:
            working_models.append('claude-code-cli')
            connection_methods.append('Local Claude CLI')

        if results['gemini_cli']['available']:
            working_models.append('gemini-cli')
            connection_methods.append('Google Cloud Shell')

        if results['huggingface']['available']:
            working_models.extend(['qwen2.5-7b-instruct', 'qwen2.5-14b-instruct', 'qwen2.5-32b-instruct'])
            connection_methods.append('HuggingFace API')

        results['summary'] = {
            'total_models': len(working_models),
            'working_models': working_models,
            'connection_methods': connection_methods,
            'status': 'ready' if working_models else 'no_models'
        }

        return results

    def _validate_claude_cli(self) -> Dict[str, any]:
        """Validate Claude CLI connection."""
        result = self.cli_detector.detect_claude_code_cli()
        return {
            'available': result.get('available', False),
            'command': 'claude',
            'subscription': 'Claude Code max plan' if result.get('available') else None,
            'reason': result.get('reason') if not result.get('available') else None
        }

    def _validate_gemini_cli(self) -> Dict[str, any]:
        """Validate Gemini CLI connection."""
        result = self.cli_detector.detect_gemini_cli()
        return {
            'available': result.get('available', False),
            'account': result.get('authenticated_account'),
            'access_method': 'gcloud cloud-shell ssh',
            'subscription': 'Google Cloud developer rates' if result.get('available') else None,
            'reason': result.get('reason') if not result.get('available') else None
        }

    def _validate_huggingface(self) -> Dict[str, any]:
        """Validate HuggingFace API connection."""
        try:
            hf_key = os.getenv('HUGGINGFACE_API_KEY', '')
            available = bool(hf_key and hf_key.startswith('hf_') and len(hf_key) > 10)

            return {
                'available': available,
                'key_preview': f"hf_***{hf_key[-4:]}" if available else None,
                'models': ['qwen2.5-7b-instruct', 'qwen2.5-14b-instruct', 'qwen2.5-32b-instruct'] if available else [],
                'reason': 'No valid HuggingFace API key found' if not available else None
            }
        except Exception as e:
            return {
                'available': False,
                'reason': f'Error checking HuggingFace: {e}'
            }

    def display_validation_summary(self, results: Dict[str, any]) -> None:
        """Display validation results in rich format."""
        console = Console()

        # Header
        console.print(Panel.fit(
            "[bold blue]🔗 Model Connection Validation[/bold blue]",
            border_style="blue"
        ))
        console.print()

        # Create connection status table
        table = Table(title="Available Models", show_header=True, header_style="bold magenta")
        table.add_column("Model", style="cyan", no_wrap=True)
        table.add_column("Connection", style="green")
        table.add_column("Status", justify="center")

        # Add CLI models
        if results['claude_cli']['available']:
            table.add_row(
                "claude-code-cli",
                f"Local: {results['claude_cli']['command']}",
                "✅ Ready"
            )

        if results['gemini_cli']['available']:
            table.add_row(
                "gemini-cli",
                f"Cloud Shell: {results['gemini_cli']['account']}",
                "✅ Ready"
            )

        # Add HuggingFace models
        if results['huggingface']['available']:
            for model in results['huggingface']['models']:
                table.add_row(
                    model,
                    f"HuggingFace: {results['huggingface']['key_preview']}",
                    "✅ Ready"
                )

        console.print(table)
        console.print()

        # Summary panel
        summary = results['summary']
        summary_text = Text()
        summary_text.append(f"🎯 Total Models: {summary['total_models']}\n", style="bold")
        summary_text.append(f"🔧 Connection Methods: {len(summary['connection_methods'])}\n")

        if summary['status'] == 'ready':
            summary_text.append("✅ System Status: Ready for production tasks", style="bold green")
        else:
            summary_text.append("❌ System Status: No models available", style="bold red")

        console.print(Panel(summary_text, title="[bold]Validation Summary[/bold]", border_style="green"))
        console.print()

    def display_unavailable_models(self, results: Dict[str, any]) -> None:
        """Display information about unavailable models."""
        console = Console()
        unavailable = []

        if not results['claude_cli']['available']:
            unavailable.append(f"Claude CLI: {results['claude_cli']['reason']}")

        if not results['gemini_cli']['available']:
            unavailable.append(f"Gemini CLI: {results['gemini_cli']['reason']}")

        if not results['huggingface']['available']:
            unavailable.append(f"HuggingFace: {results['huggingface']['reason']}")

        if unavailable:
            console.print(Panel(
                "\n".join([f"⚠️ {item}" for item in unavailable]),
                title="[yellow]Unavailable Connections[/yellow]",
                border_style="yellow"
            ))
            console.print()


def validate_and_display_models() -> Dict[str, any]:
    """Main function to validate and display models."""
    validator = ModelValidator()
    results = validator.validate_all_models()

    validator.display_validation_summary(results)

    # Show unavailable models if any
    validator.display_unavailable_models(results)

    return results


if __name__ == "__main__":
    validate_and_display_models()