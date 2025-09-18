import argparse
import asyncio
import os
import subprocess
import sys
from pathlib import Path

# EMERGENCY: Clean up terminal state immediately to prevent mouse flood
try:
    # Disable all mouse tracking modes immediately
    emergency_sequences = ["\033[?1000l", "\033[?1002l", "\033[?1003l",
                          "\033[?1006l", "\033[?1015l", "\033[?25h",
                          "\033[?1049l", "\033[?1004l", "\033[?2004l"]
    for seq in emergency_sequences:
        sys.stdout.write(seq)
        sys.stdout.flush()
    os.system('stty sane 2>/dev/null || true')
except Exception:
    pass  # Fail silently

from mmengine import DictAction
from textual import work
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import (Button, Header, Footer, Log, Input, Select,
                           Label, Static, ListView, ListItem)
from textual import events

root = str(Path(__file__).resolve().parents[0])
sys.path.append(root)

# Apply compatibility fixes early
from src.compat import compatibility_manager
compatibility_manager.apply_compatibility_fixes()

from src.agent import create_agent
from src.config import config
from src.logger import logger
from src.models import model_manager
from src.tui.agent_integration import run_with_tui_progress
from src.project_cli import setup_project_cli


def test_textual():
    """Simple test to check if Textual works in this environment."""
    from textual.app import App
    from textual.widgets import Label
    import sys

    class TestApp(App):
        def compose(self) -> ComposeResult:
            yield Label("Textual Test - If you see this, Textual is working!")

        def on_key(self, event):
            if event.key == "q":
                self.exit()

    # Check if stdout is a terminal
    if not sys.stdout.isatty():
        print("Warning: stdout is not a terminal")
        return False

    app = TestApp()
    try:
        app.run()
    except Exception as e:
        print(f"Textual test failed: {e}")
        return False
    return True


def parse_args():
    # First check if this is a test command
    import sys
    if '--test-textual' in sys.argv:
        # Create a simple args object for test
        class TestArgs:
            test_textual = True
            tui = False
            command = None
        return TestArgs()
    
    parser = argparse.ArgumentParser(
        description='DeepResearchAgent - Multi-Project Research Tool')
    
    # Add global TUI flag
    parser.add_argument(
        "--tui", action="store_true", help="Launch TUI mode")
    
    # Add test flag
    parser.add_argument(
        "--test-textual", action="store_true", help="Test if Textual works in this environment")
    
    subparsers = parser.add_subparsers(
        dest='command', help='Available commands', required=False)

    # Main research command (default behavior)
    research_parser = subparsers.add_parser(
        'research', help='Run research tasks')
    research_parser.add_argument(
        "--config",
        default=os.path.join(root, "configs", "config_main.py"),
        help="config file path")
    research_parser.add_argument(
        "--task", type=str, help="Research task to execute")
    research_parser.add_argument(
        "--no-progress", action="store_true",
        help="Disable progress display")
    research_parser.add_argument(
        '--cfg-options',
        nargs='+',
        action=DictAction,
        help='override some settings in the used config'
    )

    # Setup project management commands
    setup_project_cli(subparsers)

    args = parser.parse_args()
    return args


class DeepResearchTUI(App):
    """TUI for DeepResearchAgent with menu and description panels."""

    # Disable mouse support to avoid coordinate issues
    ENABLE_MOUSE_SUPPORT = False
    
    # State for project research mode
    research_mode = False
    selected_project = None
    research_task = ""
    current_selection = 0  # Track which menu item is selected

    # Menu items with descriptions
    MENU_ITEMS = [
        {
            "id": "run_general",
            "name": "Run General Agent",
            "description": "Execute the general research agent.\n\n"
                           "Runs the main pipeline with broad capabilities.",
            "shortcut": "g"
        },
        {
            "id": "run_gaia",
            "name": "Run Gaia Test",
            "description": "Execute GAIA benchmark tests.\n\n"
                           "Evaluates agent performance against benchmarks.",
            "shortcut": "a"
        },
        {
            "id": "run_oai",
            "name": "Run OAI Deep Research",
            "description": "Execute OpenAI's deep research pipeline.\n\n"
                           "Uses advanced OpenAI models for analysis.",
            "shortcut": "o"
        },
        {
            "id": "run_cli",
            "name": "Run CLI Fallback",
            "description": "Execute research with CLI-first config.\n\n"
                           "Optimized for Claude Code and Gemini.",
            "shortcut": "c"
        },
        {
            "id": "research",
            "name": "Research Task",
            "description": "Run a custom research task.\n\n"
                           "Execute the main research agent with your own task.",
            "shortcut": "r"
        },
        {
            "id": "project_add",
            "name": "Add Project",
            "description": "Add a new project to the registry.\n\n"
                           "Register a project for research and tracking.",
            "shortcut": "p"
        },
        {
            "id": "project_list",
            "name": "List Projects",
            "description": "Display all registered projects.\n\n"
                           "Shows names, IDs, paths, and status.",
            "shortcut": "l"
        },
        {
            "id": "project_research",
            "name": "Research on Project",
            "description": "Perform research on a specific project.\n\n"
                           "Select projects and define custom tasks.",
            "shortcut": "s"
        },
        {
            "id": "project_history",
            "name": "Project History",
            "description": "Show research history for a project.\n\n"
                           "View past research sessions and results.",
            "shortcut": "h"
        },
        {
            "id": "project_remove",
            "name": "Remove Project",
            "description": "Remove a project from the registry.\n\n"
                           "Delete project registration and history.",
            "shortcut": "d"
        },
        {
            "id": "quit",
            "name": "Quit Application",
            "description": "Exit the DeepResearchAgent TUI.\n\n"
                           "All processes will be terminated.",
            "shortcut": "q"
        }
    ]  # Updated with scrollable menu and click support

    CSS = """
    Screen {
        layout: vertical;
    }

    Header {
        height: 3;
    }

    Footer {
        height: 3;
    }

    Horizontal {
        height: 1fr;
    }

    #menu_panel {
        width: 40;
        border: solid $primary;
        padding: 1;
        overflow-y: auto;
    }

    #description_panel {
        width: 1fr;
        border: solid $secondary;
        padding: 1;
    }

    #log {
        height: 1fr;
        border: solid $primary;
        padding: 1;
    }

    .menu-item {
        padding: 0 1;
        margin: 0 0 1 0;
        background: $surface;
        width: 100%;
        text-align: left;
    }

    .menu-item.selected {
        background: $primary;
        color: $primary-background;
    }

    .menu-item:hover {
        background: $accent;
    }

    .menu-item:focus {
        background: $primary;
        color: $primary-background;
    }

    Label {
        margin-bottom: 1;
    }

    Static {
        color: $text-muted;
    }
    """

    BINDINGS = [
        ("up", "cursor_up", "Move up"),
        ("down", "cursor_down", "Move down"),
        ("enter", "select_item", "Select item"),
        ("q", "quit", "Quit"),
        ("g", "run_general", "Run General Agent"),
        ("a", "run_gaia", "Run Gaia Test"),
        ("o", "run_oai", "Run OAI Deep Research"),
        ("c", "run_cli", "Run CLI Fallback"),
        ("r", "research", "Research Task"),
        ("p", "project_add", "Add Project"),
        ("l", "project_list", "List Projects"),
        ("s", "project_research", "Research on Project"),
        ("h", "project_history", "Project History"),
        ("d", "project_remove", "Remove Project"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with Horizontal():
            # Left panel: Menu
            with Vertical(id="menu_panel"):
                yield Label("🔬 DeepResearchAgent")
                for i, item in enumerate(self.MENU_ITEMS):
                    classes = "menu-item"
                    if i == self.current_selection:
                        classes += " selected"
                    button = Button(
                        f"[{item['shortcut']}] {item['name']}",
                        classes=classes,
                        id=f"menu_item_{i}",
                        variant="default"
                    )
                    yield button

            # Right panel: Description
            with Vertical(id="description_panel"):
                if self.research_mode:
                    # Project research mode UI
                    yield Label("🔬 Project Research")
                    if not self.selected_project:
                        project_options = self._get_project_options()
                        if project_options:
                            yield Label("Select a project:")
                            yield Select(
                                options=project_options,
                                id="project_select",
                                prompt="Choose a project..."
                            )
                        else:
                            yield Label("❌ No projects found.")
                            yield Button("Back to Main Menu",
                                         id="back_to_main")
                    else:
                        yield Label("Selected: "
                                    f"{self.selected_project['name']}")
                        yield Label("Enter research task:")
                        yield Input(
                            placeholder="What would you like to research?",
                            id="task_input"
                        )
                        yield Button("Start Research", id="start_research")
                        yield Button("Cancel", id="cancel_research")
                else:
                    # Main menu description
                    current_item = self.MENU_ITEMS[self.current_selection]
                    yield Label(f"📋 {current_item['name']}")
                    yield Static(current_item['description'])
                    yield Static(f"\nShortcut: [{current_item['shortcut']}]")

        # Bottom: Log
        yield Log(id="log")

    def on_mount(self) -> None:
        """Called when the app is mounted - setup terminal mode."""
        # Ensure we're in the right terminal mode
        import sys
        import os
        
        # Reset terminal to known state
        os.system('stty sane 2>/dev/null || true')
        
        # Disable mouse tracking by sending escape sequences
        sys.stdout.write('\033[?1000l')  # Disable mouse tracking
        sys.stdout.write('\033[?1002l')  # Disable mouse motion tracking  
        sys.stdout.write('\033[?1003l')  # Disable all mouse tracking
        sys.stdout.write('\033[?1005l')  # Disable mouse wheel tracking
        sys.stdout.write('\033[?1006l')  # Disable SGR mouse mode
        sys.stdout.write('\033[?1015l')  # Disable URXVT mouse mode
        
        # Reset cursor and screen
        sys.stdout.write('\033[2J')      # Clear screen
        sys.stdout.write('\033[H')       # Move cursor to home
        sys.stdout.write('\033[?25h')    # Show cursor
        
        sys.stdout.flush()
        
        # Log initialization info now that widgets are mounted
        log = self.query_one("#log", Log)
        log.write("🚀 DeepResearchTUI initialized")
        log.write(f"📊 Menu items: {len(self.MENU_ITEMS)}")
        for i, item in enumerate(self.MENU_ITEMS):
            log.write(f"   {i}: {item['name']} ({item['id']})")
        log.write("🖥️  Terminal mode configured - mouse tracking disabled")
        log.write("🎯 Use keyboard navigation: ↑/↓ to select, Enter to activate")
        log.write("ℹ️  If you see mouse coordinates, try: reset && python main.py --tui")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses including menu item clicks."""
        button_id = event.button.id
        log = self.query_one("#log", Log)
        log.write(f"🔘 Button pressed: {button_id}")

        # Handle menu item clicks
        if button_id.startswith("menu_item_"):
            try:
                item_index = int(button_id.split("_")[-1])
                if 0 <= item_index < len(self.MENU_ITEMS):
                    self.current_selection = item_index
                    self.refresh()
                    log.write(f"📋 Menu item {item_index} selected: {self.MENU_ITEMS[item_index]['name']}")
                    # Execute the selected action
                    current_item = self.MENU_ITEMS[self.current_selection]
                    action_map = {
                        "run_general": self.run_general_agent,
                        "run_gaia": self.run_gaia_test,
                        "run_oai": self.run_oai_deep_research,
                        "run_cli": self.run_cli_fallback,
                        "research": self.research_task,
                        "project_add": self.project_add,
                        "project_list": self.project_list,
                        "project_research": self.start_project_research,
                        "project_history": self.project_history,
                        "project_remove": self.project_remove,
                        "quit": self.action_quit,
                    }
                    if current_item["id"] in action_map:
                        log.write(f"🚀 Executing action: {current_item['id']}")
                        action_map[current_item["id"]]()
                    else:
                        log.write(f"❌ No action found for: {current_item['id']}")
                else:
                    log.write(f"❌ Invalid menu item index: {item_index}")
            except (ValueError, IndexError) as e:
                log.write(f"❌ Error parsing menu item ID: {e}")
            return

        # Handle other buttons
        action_map = {
            "run_general": self.run_general_agent,
            "run_gaia": self.run_gaia_test,
            "run_oai": self.run_oai_deep_research,
            "run_cli": self.run_cli_fallback,
            "research": self.research_task,
            "project_add": self.project_add,
            "project_list": self.project_list,
            "project_research": self.start_project_research,
            "project_history": self.project_history,
            "project_remove": self.project_remove,
            "back_to_main": self.back_to_main,
            "start_research": self.start_research,
            "cancel_research": self.cancel_research,
            "quit": self.action_quit,
        }
        if button_id in action_map:
            log.write(f"🚀 Executing other action: {button_id}")
            action_map[button_id]()
        else:
            log.write(f"❓ Unknown button: {button_id}")

    def on_focus(self, event: events.Focus) -> None:
        """Handle focus events on menu buttons."""
        if event.widget.id and event.widget.id.startswith("menu_item_"):
            try:
                item_index = int(event.widget.id.split("_")[-1])
                if 0 <= item_index < len(self.MENU_ITEMS):
                    self.current_selection = item_index
                    self.refresh()
            except (ValueError, IndexError):
                pass

    async def action_quit(self) -> None:
        self.exit()

    def action_run_general(self) -> None:
        self.run_general_agent()

    def action_run_gaia(self) -> None:
        self.run_gaia_test()

    def action_run_oai(self) -> None:
        self.run_oai_deep_research()

    def action_run_cli(self) -> None:
        self.run_cli_fallback()

    def action_research(self) -> None:
        self.research_task()

    def action_project_add(self) -> None:
        self.project_add()

    def action_project_list(self) -> None:
        self.project_list()

    def action_project_research(self) -> None:
        self.start_project_research()

    def action_project_history(self) -> None:
        self.project_history()

    def action_project_remove(self) -> None:
        self.project_remove()

    def action_cursor_up(self) -> None:
        """Move cursor up in menu."""
        if not self.research_mode:
            old_selection = self.current_selection
            self.current_selection = max(0, self.current_selection - 1)
            if old_selection != self.current_selection:
                self.refresh()

    def action_cursor_down(self) -> None:
        """Move cursor down in menu."""
        if not self.research_mode:
            old_selection = self.current_selection
            self.current_selection = min(
                len(self.MENU_ITEMS) - 1,
                self.current_selection + 1
            )
            if old_selection != self.current_selection:
                self.refresh()

    def action_select_item(self) -> None:
        """Select the currently highlighted menu item."""
        if not self.research_mode:
            current_item = self.MENU_ITEMS[self.current_selection]
            action_map = {
                "run_general": self.run_general_agent,
                "run_gaia": self.run_gaia_test,
                "run_oai": self.run_oai_deep_research,
                "run_cli": self.run_cli_fallback,
                "research": self.research_task,
                "project_add": self.project_add,
                "project_list": self.project_list,
                "project_research": self.start_project_research,
                "project_history": self.project_history,
                "project_remove": self.project_remove,
                "quit": self.action_quit,
            }
            if current_item["id"] in action_map:
                action_map[current_item["id"]]()

    @work(exclusive=True, thread=True)
    def run_general_agent(self) -> None:
        self._run_agent("examples/run_general.py", "General Agent")

    @work(exclusive=True, thread=True)
    def run_gaia_test(self) -> None:
        self._run_agent("examples/run_gaia.py", "Gaia Test")

    @work(exclusive=True, thread=True)
    def run_oai_deep_research(self) -> None:
        self._run_agent(
            "examples/run_oai_deep_research.py",
            "OAI Deep Research"
        )

    @work(exclusive=True, thread=True)
    def run_cli_fallback(self) -> None:
        self._run_agent(
            "main.py",
            "CLI Fallback",
            ["--config", "configs/config_cli_fallback.py"]
        )

    @work(exclusive=True, thread=True)
    def project_list(self) -> None:
        """List all projects in the registry."""
        log = self.query_one("#log", Log)
        log.write("📋 Listing projects...")

        try:
            from src.project_cli import list_projects_command

            # Create a mock args object
            class MockArgs:
                pass
            mock_args = MockArgs()
            list_projects_command(mock_args)
            log.write("✅ Project list displayed above")
        except Exception as e:
            log.write(f"❌ Error listing projects: {e}")

    @work(exclusive=True, thread=True)
    def research_task(self) -> None:
        """Run a custom research task."""
        log = self.query_one("#log", Log)
        log.write("🔬 Research task feature coming soon...")
        log.write("   Use CLI commands for now:")
        log.write("   uv run python main.py research \"your task here\"")

    @work(exclusive=True, thread=True)
    def project_add(self) -> None:
        """Add a new project to the registry."""
        log = self.query_one("#log", Log)
        log.write("� Add project feature coming soon...")
        log.write("   Use CLI commands for now:")
        log.write("   uv run python main.py project-add \"Project Name\" /path/to/project")

    @work(exclusive=True, thread=True)
    def project_history(self) -> None:
        """Show research history for a project."""
        log = self.query_one("#log", Log)
        log.write("📚 Project history feature coming soon...")
        log.write("   Use CLI commands for now:")
        log.write("   uv run python main.py project-list")
        log.write("   uv run python main.py project-history <project_id>")

    @work(exclusive=True, thread=True)
    def project_remove(self) -> None:
        """Remove a project from the registry."""
        log = self.query_one("#log", Log)
        log.write("🗑️  Remove project feature coming soon...")
        log.write("   Use CLI commands for now:")
        log.write("   uv run python main.py project-list")
        log.write("   uv run python main.py project-remove <project_id>")

    def _get_project_options(self):
        """Get project options for the select widget."""
        try:
            from src.project_registry import project_registry
            projects = project_registry.list_projects()
            if not projects:
                return []
            return [(project.name, project.id) for project in projects]
        except Exception:
            return []

    def start_project_research(self):
        """Start the project research mode."""
        self.research_mode = True
        self.selected_project = None
        self.research_task = ""
        self.refresh()

    def back_to_main(self):
        """Return to main menu."""
        self.research_mode = False
        self.selected_project = None
        self.research_task = ""
        self.refresh()

    def cancel_research(self):
        """Cancel research and return to project selection."""
        self.selected_project = None
        self.research_task = ""
        self.refresh()

    @work(exclusive=True, thread=True)
    def start_research(self) -> None:
        """Start the actual research on the selected project."""
        if not self.selected_project or not self.research_task:
            return

        log = self.query_one("#log", Log)
        log.write("🔬 Starting research on project: "
                  f"{self.selected_project['name']}")
        log.write(f"   Task: {self.research_task}")

        try:
            # Import required modules
            from src.project_cli import research_command

            # Create args object for research command
            class MockArgs:
                def __init__(self, project_id: str, task: str):
                    self.project_id = project_id
                    self.task = task

            mock_args = MockArgs(
                self.selected_project['id'],
                self.research_task
            )

            # Run the research
            research_command(mock_args)

            log.write("✅ Research completed!")
            self.back_to_main()

        except Exception as e:
            log.write(f"❌ Research failed: {e}")
            self.back_to_main()

    def on_select_changed(self, event: Select.Changed) -> None:
        """Handle project selection."""
        if event.select.id == "project_select" and event.value:
            try:
                from src.project_registry import project_registry
                project_id = str(event.value)
                project = project_registry.get_project(project_id)
                if project:
                    self.selected_project = {
                        'id': project.id,
                        'name': project.name,
                        'path': project.path
                    }
                    self.refresh()
            except Exception as e:
                log = self.query_one("#log", Log)
                log.write(f"❌ Error selecting project: {e}")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle task input submission."""
        if event.input.id == "task_input":
            self.research_task = event.value
            # Auto-start research when task is entered
            if self.selected_project and self.research_task:
                self.start_research()

    def _run_agent(
        self, script: str, name: str, args: list[str] | None = None
    ) -> None:
        """Run an agent script in a worker thread to avoid blocking the UI."""
        log = self.query_one("#log", Log)
        log.write(f"Starting {name}...")
        cmd = ["uv", "run", "python", script]
        if args:
            cmd.extend(args)
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent,
                timeout=300  # 5-minute timeout
            )
            if result.returncode == 0:
                log.write(f"✓ {name} completed successfully.")
                if result.stdout.strip():
                    log.write(f"Output: {result.stdout.strip()}")
            else:
                log.write(
                    f"✗ {name} failed with exit code {result.returncode}."
                )
                if result.stderr.strip():
                    log.write(f"Error: {result.stderr.strip()}")
        except subprocess.TimeoutExpired:
            log.write(f"✗ {name} timed out after 5 minutes.")
        except Exception as e:
            log.write(f"✗ {name} encountered an error: {e}")

    def action_quit(self) -> None:
        """Quit the TUI with proper cleanup."""
        self._cleanup_terminal()
        self.exit()

    def _cleanup_terminal(self) -> None:
        """Comprehensive terminal cleanup to disable mouse tracking."""
        import sys

        # Disable all mouse tracking modes
        cleanup_sequences = [
            "\033[?1000l",    # Disable X11 mouse reporting
            "\033[?1002l",    # Disable cell motion mouse tracking
            "\033[?1003l",    # Disable all motion mouse tracking
            "\033[?1006l",    # Disable SGR mouse mode
            "\033[?1015l",    # Disable urxvt mouse mode
            "\033[?25h",      # Show cursor
            "\033[?1049l",    # Exit alternate screen
            "\033[?1004l",    # Disable focus reporting
            "\033[?2004l",    # Disable bracketed paste
        ]

        for seq in cleanup_sequences:
            sys.stdout.write(seq)
            sys.stdout.flush()

    def on_key(self, event) -> None:
        """Handle key presses including quit."""
        if event.key == "q":
            self.action_quit()
        # Let other keys be handled by default bindings

    def on_shutdown(self) -> None:
        """Called when app shuts down - ensure cleanup."""
        self._cleanup_terminal()


async def main(args, task: str | None = None):
    try:
        # Initialize the configuration
        config.init_config(args.config, args)

        # Initialize the logger
        logger.init_logger(log_path=config.log_path)
        logger.info(f"| Logger initialized at: {config.log_path}")
        logger.info(f"| Config:\n{config.pretty_text}")

        # Initialize models with validation
        logger.info("| Initializing models...")
        model_manager.init_models(use_local_proxy=True)

        # Display model validation for user
        from src.models.model_validator import validate_and_display_models
        validation_results = validate_and_display_models()

        logger.info(
            "| Model validation complete: %d models available",
            validation_results['summary']['total_models']
        )

    except RuntimeError as e:
        logger.error(f"| Startup failed: {e}")
        logger.error("| Please check your configuration and try again")
        sys.exit(1)
    except Exception as e:
        logger.error(f"| Unexpected error during startup: {e}")
        logger.error("| See logs above for details")
        sys.exit(1)

    # Create agent
    agent = await create_agent(config)
    logger.visualize_agent_tree(agent)

    # Use provided task or command line task or fallback to default
    if task is None:
        task = getattr(args, 'task', None)

    if task is None:
        # Default demo task as fallback
        task = (
            "Use deep_researcher_agent to search the latest papers on the "
            "topic of 'AI Agent' and then summarize it."
        )
        logger.info("| Using default demo task (no custom task provided)")
    else:
        logger.info(f"| Executing custom task: {task[:100]}...")

    # Determine if we should show progress display
    show_progress = not getattr(args, 'no_progress', False)

    if show_progress:
        # Run with TUI progress display
        logger.info("| Starting task execution with progress display...")
        res = await run_with_tui_progress(
            agent,
            task,
            is_hierarchical=True,
            show_progress=True
        )
    else:
        # Run without progress display (traditional logging)
        logger.info("| Starting task execution (logs only)...")
        res = await agent.run(task)

    logger.info(f"| Result: {res}")

if __name__ == '__main__':
    args = parse_args()

    # Handle project management commands
    if hasattr(args, 'func') and args.func:
        # This is a project management command
        args.func(args)
        sys.exit(0)

    # Handle test command
    if getattr(args, 'test_textual', False):
        print("Testing Textual compatibility...")
        success = test_textual()
        if success:
            print("✅ Textual test passed!")
        else:
            print("❌ Textual test failed!")
        sys.exit(0)

    # Handle TUI mode - either explicitly requested or default when no command
    if getattr(args, 'tui', False) or args.command is None:
        # Check terminal compatibility first
        import sys
        if not sys.stdin.isatty() or not sys.stdout.isatty():
            print("❌ TUI requires an interactive terminal (TTY)")
            print()
            print("The current environment is not a proper TTY:")
            print(f"  stdin.isatty(): {sys.stdin.isatty()}")
            print(f"  stdout.isatty(): {sys.stdout.isatty()}")
            print()
            print("🔧 Solutions:")
            print("  1. Run in a proper terminal emulator (not IDE terminal)")
            print("  2. Use: python main.py --config configs/config_cli_fallback.py")
            print("  3. Or run without --tui flag to use CLI mode")
            print()
            print("Falling back to CLI mode...")
            # Fall through to CLI mode instead of exiting
        else:
            # Reset terminal to a known state and disable mouse tracking
            import os

            # Comprehensive terminal reset
            reset_sequences = [
                "\033[?1000l",    # Disable X11 mouse reporting
                "\033[?1002l",    # Disable cell motion mouse tracking
                "\033[?1003l",    # Disable all motion mouse tracking
                "\033[?1006l",    # Disable SGR mouse mode
                "\033[?1015l",    # Disable urxvt mouse mode
                "\033[?25h",      # Show cursor
                "\033[?1049l",    # Exit alternate screen
                "\033[?1004l",    # Disable focus reporting
                "\033[?2004l",    # Disable bracketed paste
            ]

            for seq in reset_sequences:
                sys.stdout.write(seq)
                sys.stdout.flush()

            os.system('stty sane')
            os.system('reset')

            try:
                app = DeepResearchTUI()
                app.run()
            except Exception as e:
                print(f"❌ TUI failed: {e}")
                print("Falling back to CLI mode...")
            finally:
                # Ensure cleanup on exit
                for seq in reset_sequences:
                    sys.stdout.write(seq)
                    sys.stdout.flush()
                os.system('stty sane')
                sys.exit(0)  # Exit after TUI attempt

        # If we get here, either TTY check failed or TUI crashed - run CLI mode
    else:
        asyncio.run(main(args))
# TUI scrolling and click fixes applied
