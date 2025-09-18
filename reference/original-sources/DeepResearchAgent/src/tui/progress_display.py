"""
Progress display module for real-time agent execution monitoring
"""

import asyncio
import signal
import time
from typing import Dict, List, Optional, Callable, Any
from enum import Enum
from dataclasses import dataclass

from rich.console import Console
from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    SpinnerColumn,
    TaskID
)
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.text import Text


class AgentStatus(Enum):
    """Agent execution status"""
    WAITING = "waiting"
    ACTIVE = "active"
    COMPLETE = "complete"
    ERROR = "error"
    CANCELLED = "cancelled"


class TaskPhase(Enum):
    """Task execution phases"""
    INITIALIZING = "initializing"
    PLANNING = "planning"
    RESEARCH = "research"
    ANALYSIS = "analysis"
    SUMMARY = "summary"
    COMPLETE = "complete"


@dataclass
class AgentState:
    """Agent execution state"""
    name: str
    status: AgentStatus
    current_step: str = ""
    progress: float = 0.0
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    error_message: Optional[str] = None


@dataclass
class TaskProgress:
    """Overall task progress state"""
    phase: TaskPhase
    overall_progress: float = 0.0
    start_time: float = time.time()
    estimated_total_time: Optional[float] = None
    agents: Dict[str, AgentState] = None

    def __post_init__(self):
        if self.agents is None:
            self.agents = {}


class ProgressDisplayManager:
    """
    Manages real-time progress display for agent execution
    """

    def __init__(self):
        self.console = Console()
        self.task_progress = TaskProgress(TaskPhase.INITIALIZING)
        self.progress_bars = None
        self.live_display = None
        self.is_cancelled = False
        self.cancel_callback: Optional[Callable] = None

        # Progress tracking
        self.overall_task_id: Optional[TaskID] = None
        self.agent_task_ids: Dict[str, TaskID] = {}

        # Setup signal handlers for graceful shutdown
        self._setup_signal_handlers()

    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful interruption"""
        def signal_handler(signum, frame):
            self.console.print("\n[yellow]⚠️  Interrupt received. Gracefully shutting down...[/yellow]")
            self.request_cancellation()

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    def set_cancel_callback(self, callback: Callable):
        """Set callback function to call when cancellation is requested"""
        self.cancel_callback = callback

    def request_cancellation(self):
        """Request graceful cancellation of current task"""
        self.is_cancelled = True
        if self.cancel_callback:
            asyncio.create_task(self.cancel_callback())

    def initialize_agents(self, agent_names: List[str]):
        """Initialize agent states for tracking"""
        for name in agent_names:
            self.task_progress.agents[name] = AgentState(
                name=name,
                status=AgentStatus.WAITING
            )

    def update_phase(self, phase: TaskPhase, estimated_time: Optional[float] = None):
        """Update current task phase"""
        self.task_progress.phase = phase
        if estimated_time:
            self.task_progress.estimated_total_time = estimated_time

    def update_agent_status(self, agent_name: str, status: AgentStatus,
                          step: str = "", progress: float = 0.0, error: str = None):
        """Update agent execution status"""
        if agent_name not in self.task_progress.agents:
            self.task_progress.agents[agent_name] = AgentState(agent_name, status)

        agent = self.task_progress.agents[agent_name]
        agent.status = status
        agent.current_step = step
        agent.progress = progress
        agent.error_message = error

        if status == AgentStatus.ACTIVE and agent.start_time is None:
            agent.start_time = time.time()
        elif status in [AgentStatus.COMPLETE, AgentStatus.ERROR, AgentStatus.CANCELLED]:
            agent.end_time = time.time()

        # Update progress bars if initialized
        if self.progress_bars and agent_name in self.agent_task_ids:
            task_id = self.agent_task_ids[agent_name]
            self.progress_bars.update(task_id, completed=progress)

    def update_overall_progress(self, progress: float):
        """Update overall task progress"""
        self.task_progress.overall_progress = progress
        if self.progress_bars and self.overall_task_id:
            self.progress_bars.update(self.overall_task_id, completed=progress)

    def _create_progress_display(self) -> Layout:
        """Create the main progress display layout"""
        layout = Layout()

        # Create progress bars
        self.progress_bars = Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            console=self.console,
            expand=True
        )

        # Add overall progress
        self.overall_task_id = self.progress_bars.add_task(
            f"[green]Overall: {self.task_progress.phase.value.title()}",
            total=100
        )

        # Add agent progress bars
        for agent_name, agent in self.task_progress.agents.items():
            status_color = self._get_status_color(agent.status)
            task_id = self.progress_bars.add_task(
                f"[{status_color}]{agent_name}: {agent.current_step or 'Waiting'}",
                total=100
            )
            self.agent_task_ids[agent_name] = task_id

        # Create agent status table
        status_table = self._create_status_table()

        # Create layout
        layout.split_column(
            Layout(Panel(self.progress_bars, title="🤖 Agent Execution Progress"), size=8),
            Layout(Panel(status_table, title="📊 Agent Status Details"), size=6)
        )

        return layout

    def _create_status_table(self) -> Table:
        """Create agent status details table"""
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Agent", style="bold", width=20)
        table.add_column("Status", width=12)
        table.add_column("Current Step", width=30)
        table.add_column("Progress", width=10)
        table.add_column("Runtime", width=12)

        for agent_name, agent in self.task_progress.agents.items():
            status_text = Text(agent.status.value.title())
            status_text.stylize(self._get_status_color(agent.status))

            # Calculate runtime
            if agent.start_time:
                end_time = agent.end_time or time.time()
                runtime = f"{end_time - agent.start_time:.1f}s"
            else:
                runtime = "-"

            table.add_row(
                agent_name,
                status_text,
                agent.current_step or "-",
                f"{agent.progress:.1f}%",
                runtime
            )

        return table

    def _get_status_color(self, status: AgentStatus) -> str:
        """Get color for agent status"""
        color_map = {
            AgentStatus.WAITING: "dim",
            AgentStatus.ACTIVE: "green",
            AgentStatus.COMPLETE: "blue",
            AgentStatus.ERROR: "red",
            AgentStatus.CANCELLED: "yellow"
        }
        return color_map.get(status, "white")

    async def start_monitoring(self):
        """Start real-time progress monitoring"""
        layout = self._create_progress_display()

        self.live_display = Live(
            layout,
            console=self.console,
            refresh_per_second=4,
            transient=False
        )

        self.live_display.start()

        # Update display loop
        try:
            while not self.is_cancelled and self.task_progress.phase != TaskPhase.COMPLETE:
                await asyncio.sleep(0.25)

                # Update progress bars with current state
                if self.progress_bars:
                    # Update overall progress bar description
                    if self.overall_task_id:
                        self.progress_bars.update(
                            self.overall_task_id,
                            description=f"[green]Overall: {self.task_progress.phase.value.title()}",
                            completed=self.task_progress.overall_progress
                        )

                    # Update agent progress bars
                    for agent_name, agent in self.task_progress.agents.items():
                        if agent_name in self.agent_task_ids:
                            task_id = self.agent_task_ids[agent_name]
                            status_color = self._get_status_color(agent.status)
                            description = f"[{status_color}]{agent_name}: {agent.current_step or agent.status.value.title()}"
                            self.progress_bars.update(
                                task_id,
                                description=description,
                                completed=agent.progress
                            )

                # Update status table
                layout.children[1].update(Panel(self._create_status_table(), title="📊 Agent Status Details"))

        finally:
            if self.live_display:
                self.live_display.stop()

    def stop_monitoring(self):
        """Stop progress monitoring"""
        self.is_cancelled = True
        if self.live_display:
            self.live_display.stop()

    def display_completion_summary(self, result: Optional[str] = None):
        """Display task completion summary"""
        if self.live_display:
            self.live_display.stop()

        # Calculate total runtime
        total_time = time.time() - self.task_progress.start_time

        # Create completion panel
        if self.is_cancelled:
            title = "🛑 Task Cancelled"
            content = "[yellow]Task execution was cancelled by user.[/yellow]"
            style = "yellow"
        elif any(agent.status == AgentStatus.ERROR for agent in self.task_progress.agents.values()):
            title = "❌ Task Failed"
            content = "[red]Task execution failed. Check agent details above.[/red]"
            style = "red"
        else:
            title = "✅ Task Complete"
            content = f"[green]Task completed successfully in {total_time:.1f} seconds.[/green]"
            style = "green"

        if result:
            content += f"\n\n[bold]Result:[/bold]\n{result[:200]}..."

        self.console.print(Panel(content, title=title, border_style=style))

        # Show final agent summary
        final_table = self._create_status_table()
        self.console.print(Panel(final_table, title="📊 Final Agent Status"))


# Convenience functions for easy integration

def create_progress_manager(agent_names: List[str]) -> ProgressDisplayManager:
    """Create and initialize a progress manager"""
    manager = ProgressDisplayManager()
    manager.initialize_agents(agent_names)
    return manager


async def monitor_task_progress(
    manager: ProgressDisplayManager,
    task_coroutine: Callable,
    cancel_callback: Optional[Callable] = None
) -> Any:
    """
    Monitor task progress with real-time display

    Args:
        manager: Progress display manager
        task_coroutine: Async function to execute
        cancel_callback: Function to call on cancellation

    Returns:
        Result from task_coroutine
    """
    if cancel_callback:
        manager.set_cancel_callback(cancel_callback)

    # Start monitoring in background
    monitor_task = asyncio.create_task(manager.start_monitoring())

    try:
        # Execute the main task
        result = await task_coroutine()
        manager.update_phase(TaskPhase.COMPLETE)
        manager.update_overall_progress(100)

        # Give a moment for final update
        await asyncio.sleep(0.5)

        return result

    except asyncio.CancelledError:
        manager.request_cancellation()
        raise
    except Exception as e:
        manager.console.print(f"[red]Error during task execution: {e}[/red]")
        raise
    finally:
        monitor_task.cancel()
        try:
            await monitor_task
        except asyncio.CancelledError:
            pass

        manager.stop_monitoring()


if __name__ == "__main__":
    # Test the progress display system
    async def test_progress():
        manager = create_progress_manager(["Planning Agent", "Research Agent", "Analysis Agent"])

        async def mock_task():
            manager.update_phase(TaskPhase.PLANNING)
            manager.update_agent_status("Planning Agent", AgentStatus.ACTIVE, "Creating plan", 0)

            for i in range(101):
                await asyncio.sleep(0.05)
                manager.update_agent_status("Planning Agent", AgentStatus.ACTIVE, "Creating plan", i)
                manager.update_overall_progress(i / 3)

                if manager.is_cancelled:
                    return "Cancelled"

            manager.update_agent_status("Planning Agent", AgentStatus.COMPLETE, "Plan complete", 100)
            manager.update_phase(TaskPhase.RESEARCH)
            manager.update_agent_status("Research Agent", AgentStatus.ACTIVE, "Searching", 0)

            for i in range(101):
                await asyncio.sleep(0.03)
                manager.update_agent_status("Research Agent", AgentStatus.ACTIVE, "Searching", i)
                manager.update_overall_progress(33 + (i / 3))

                if manager.is_cancelled:
                    return "Cancelled"

            manager.update_agent_status("Research Agent", AgentStatus.COMPLETE, "Research complete", 100)
            manager.update_phase(TaskPhase.ANALYSIS)
            manager.update_agent_status("Analysis Agent", AgentStatus.ACTIVE, "Analyzing", 0)

            for i in range(101):
                await asyncio.sleep(0.02)
                manager.update_agent_status("Analysis Agent", AgentStatus.ACTIVE, "Analyzing", i)
                manager.update_overall_progress(66 + (i / 3))

                if manager.is_cancelled:
                    return "Cancelled"

            manager.update_agent_status("Analysis Agent", AgentStatus.COMPLETE, "Analysis complete", 100)
            return "Mock task completed successfully!"

        result = await monitor_task_progress(manager, mock_task)
        manager.display_completion_summary(result)
        return result

    # Run test
    asyncio.run(test_progress())