"""
Task collection module for interactive task input using Rich prompts
"""

import sys
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich.syntax import Syntax


console = Console()


def validate_task(task: str) -> tuple[bool, Optional[str]]:
    """
    Validate a research task input

    Args:
        task (str): The task to validate

    Returns:
        tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    if not task or not task.strip():
        return False, "Task cannot be empty"

    task = task.strip()

    # Minimum length validation
    if len(task) < 10:
        return False, "Task must be at least 10 characters long"

    # Maximum length validation
    if len(task) > 2000:
        return False, "Task must be less than 2000 characters"

    # Basic content validation - not purely numeric
    if task.isdigit():
        return False, "Task cannot be purely numeric"

    # Basic English check - contains at least some alphabetic characters
    if not any(c.isalpha() for c in task):
        return False, "Task must contain alphabetic characters"

    return True, None


def get_task_templates() -> list[tuple[str, str]]:
    """
    Get predefined task templates

    Returns:
        list[tuple[str, str]]: List of (template_name, template_task) tuples
    """
    return [
        ("Research Latest Papers", "Use deep_researcher_agent to search the latest papers on the topic of '{topic}' and then summarize the key findings."),
        ("Analyze Website", "Use browser_use_agent to analyze the website at {url} and provide insights about its content and structure."),
        ("Compare Technologies", "Research and compare {technology1} vs {technology2}, analyzing their advantages, disadvantages, and use cases."),
        ("Market Analysis", "Conduct a comprehensive market analysis for {industry} including trends, competitors, and opportunities."),
        ("Code Review", "Analyze the code repository at {repo_url} and provide a detailed code review with suggestions for improvement."),
        ("Technical Documentation", "Create comprehensive technical documentation for {product/technology} including setup, usage, and best practices."),
        ("Competitive Analysis", "Perform a competitive analysis of {company} against its main competitors in the {industry} sector."),
        ("Literature Review", "Conduct a systematic literature review on {research_topic} from the past 3 years."),
        ("Data Analysis", "Analyze the dataset at {data_source} and provide insights, trends, and actionable recommendations."),
        ("Custom Task", "Enter your own custom research task")
    ]


def display_templates() -> None:
    """Display available task templates"""
    templates = get_task_templates()

    console.print("\n📋 [bold cyan]Available Task Templates:[/bold cyan]\n")

    for i, (name, _) in enumerate(templates, 1):
        console.print(f"  {i}. [green]{name}[/green]")

    console.print()


def get_template_choice() -> Optional[tuple[str, str]]:
    """
    Get user's template choice

    Returns:
        Optional[tuple[str, str]]: (template_name, template_task) or None if custom
    """
    templates = get_task_templates()

    while True:
        try:
            choice = Prompt.ask(
                "Select a template number (or press Enter for custom task)",
                default="10"
            )

            if not choice.strip():
                return None

            choice_num = int(choice)
            if 1 <= choice_num <= len(templates):
                name, template = templates[choice_num - 1]
                if name == "Custom Task":
                    return None
                return name, template
            else:
                console.print(f"[red]Please enter a number between 1 and {len(templates)}[/red]")
        except ValueError:
            console.print("[red]Please enter a valid number[/red]")


def customize_template(template: str) -> str:
    """
    Allow user to customize a template by filling in placeholders

    Args:
        template (str): Template with placeholders in {placeholder} format

    Returns:
        str: Customized task
    """
    import re

    # Find all placeholders like {topic}, {url}, etc.
    placeholders = re.findall(r'\{([^}]+)\}', template)

    if not placeholders:
        return template

    console.print(f"\n📝 [bold]Customize your template:[/bold]")
    console.print(f"Template: [italic]{template}[/italic]\n")

    customized = template
    for placeholder in placeholders:
        value = Prompt.ask(f"Enter value for [cyan]{placeholder}[/cyan]")
        customized = customized.replace(f"{{{placeholder}}}", value)

    return customized


def get_multiline_task() -> str:
    """
    Get multi-line task input from user

    Returns:
        str: The complete task
    """
    console.print("\n✏️  [bold]Enter your research task:[/bold]")
    console.print("[dim]  (Type your task and press Ctrl+D or Ctrl+Z to finish)[/dim]\n")

    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass

    return "\n".join(lines).strip()


def get_user_task() -> str:
    """
    Main function to collect a research task from the user

    Returns:
        str: The validated research task
    """
    console.print(Panel.fit(
        "[bold cyan]🤖 DeepResearchAgent Task Input[/bold cyan]\n" +
        "Welcome! Let's define your research task.",
        border_style="cyan"
    ))

    while True:
        # Show templates
        display_templates()

        # Get template choice
        template_choice = get_template_choice()

        if template_choice is None:
            # Custom task
            task = get_multiline_task()
        else:
            # Template task
            template_name, template = template_choice
            console.print(f"\n📋 Selected template: [green]{template_name}[/green]")
            task = customize_template(template)

        # Validate task
        is_valid, error_msg = validate_task(task)

        if not is_valid:
            console.print(f"\n[red]❌ Invalid task: {error_msg}[/red]\n")
            if not Confirm.ask("Would you like to try again?"):
                console.print("Exiting...")
                sys.exit(0)
            continue

        # Show task for confirmation
        console.print(f"\n📝 [bold]Your research task:[/bold]")
        console.print(Panel(
            task,
            border_style="green",
            title="[green]Task Preview[/green]"
        ))

        # Confirm task
        if Confirm.ask("\n✅ Proceed with this task?"):
            console.print(f"\n🚀 [green]Task confirmed! Starting research...[/green]\n")
            return task
        else:
            console.print("\n🔄 Let's try again...\n")


if __name__ == "__main__":
    # Test the task collector
    task = get_user_task()
    console.print(f"\n[bold green]Final task:[/bold green] {task}")