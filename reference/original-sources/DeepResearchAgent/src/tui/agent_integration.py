"""
Integration module for connecting progress display with agent execution
"""

import asyncio
from typing import Optional, Any

from src.tui.progress_display import (
    ProgressDisplayManager,
    TaskPhase,
    AgentStatus,
    monitor_task_progress
)


class AgentProgressWrapper:
    """
    Wrapper to integrate existing agent system with progress display
    """

    def __init__(self, agent, progress_manager: ProgressDisplayManager):
        self.agent = agent
        self.progress_manager = progress_manager
        self.agent_name = getattr(agent, 'name', agent.__class__.__name__)

    async def run_with_progress(self, task: str) -> Any:
        """
        Run agent with progress tracking
        """
        try:
            # Start agent execution
            self.progress_manager.update_agent_status(
                self.agent_name,
                AgentStatus.ACTIVE,
                "Starting execution"
            )

            # Execute the agent task
            result = await self.agent.run(task)

            # Mark as complete
            self.progress_manager.update_agent_status(
                self.agent_name,
                AgentStatus.COMPLETE,
                "Execution complete",
                100.0
            )

            return result

        except Exception as e:
            # Mark as error
            self.progress_manager.update_agent_status(
                self.agent_name,
                AgentStatus.ERROR,
                f"Error: {str(e)[:50]}",
                error=str(e)
            )
            raise


async def run_agent_with_progress(
    agent,
    task: str,
    show_progress: bool = True,
    agent_names: Optional[list] = None
) -> Any:
    """
    Run a single agent with progress display

    Args:
        agent: The agent to run
        task: Task to execute
        show_progress: Whether to show progress display
        agent_names: List of all agent names for context

    Returns:
        Agent execution result
    """
    if not show_progress:
        return await agent.run(task)

    # Determine agent names
    if agent_names is None:
        agent_names = [getattr(agent, 'name', agent.__class__.__name__)]

    # Create progress manager
    progress_manager = ProgressDisplayManager()
    progress_manager.initialize_agents(agent_names)

    # Wrap agent with progress tracking
    wrapped_agent = AgentProgressWrapper(agent, progress_manager)

    # Set up task execution
    async def execute_task():
        progress_manager.update_phase(TaskPhase.PLANNING)
        progress_manager.update_overall_progress(10)

        result = await wrapped_agent.run_with_progress(task)

        progress_manager.update_phase(TaskPhase.COMPLETE)
        progress_manager.update_overall_progress(100)

        return result

    # Monitor progress
    result = await monitor_task_progress(progress_manager, execute_task)
    progress_manager.display_completion_summary(str(result)[:200] if result else None)

    return result


async def run_hierarchical_agent_with_progress(
    agent,
    task: str,
    show_progress: bool = True
) -> Any:
    """
    Run hierarchical agent system with progress display

    Args:
        agent: The hierarchical agent (e.g., planning agent)
        task: Task to execute
        show_progress: Whether to show progress display

    Returns:
        Agent execution result
    """
    if not show_progress:
        return await agent.run(task)

    # Extract managed agent names
    managed_agents = getattr(agent, 'managed_agents', [])
    agent_names = [getattr(agent, 'name', 'Planning Agent')]

    # Add managed agent names
    for managed_agent in managed_agents:
        if hasattr(managed_agent, 'name'):
            agent_names.append(managed_agent.name)
        else:
            agent_names.append(managed_agent.__class__.__name__)

    # Create progress manager
    progress_manager = ProgressDisplayManager()
    progress_manager.initialize_agents(agent_names)

    # Set up cancellation callback
    async def cancel_execution():
        """Cancel agent execution gracefully"""
        # Try to cancel the agent if it supports cancellation
        if hasattr(agent, 'cancel'):
            await agent.cancel()

    # Set up task execution with phase tracking
    async def execute_hierarchical_task():
        try:
            # Phase 1: Planning
            progress_manager.update_phase(TaskPhase.PLANNING)
            progress_manager.update_agent_status(
                agent_names[0],  # Main planning agent
                AgentStatus.ACTIVE,
                "Analyzing task and creating plan"
            )
            progress_manager.update_overall_progress(10)

            # Simulate planning phase progress
            for i in range(5):
                if progress_manager.is_cancelled:
                    raise asyncio.CancelledError("Task cancelled during planning")
                await asyncio.sleep(0.1)
                progress_manager.update_agent_status(
                    agent_names[0],
                    AgentStatus.ACTIVE,
                    f"Planning step {i+1}/5",
                    (i + 1) * 20
                )

            # Phase 2: Execution (this is where the real agent work happens)
            progress_manager.update_phase(TaskPhase.RESEARCH)
            progress_manager.update_overall_progress(20)

            # Execute the actual agent task
            result = await agent.run(task)

            # Phase 3: Completion
            progress_manager.update_phase(TaskPhase.COMPLETE)
            progress_manager.update_agent_status(
                agent_names[0],
                AgentStatus.COMPLETE,
                "Task completed successfully",
                100
            )
            progress_manager.update_overall_progress(100)

            return result

        except asyncio.CancelledError:
            # Handle cancellation gracefully
            for agent_name in agent_names:
                progress_manager.update_agent_status(
                    agent_name,
                    AgentStatus.CANCELLED,
                    "Cancelled by user"
                )
            raise

        except Exception as e:
            # Handle errors
            progress_manager.update_agent_status(
                agent_names[0],
                AgentStatus.ERROR,
                f"Error: {str(e)[:50]}",
                error=str(e)
            )
            raise

    # Monitor progress with cancellation support
    result = await monitor_task_progress(
        progress_manager,
        execute_hierarchical_task,
        cancel_execution
    )

    progress_manager.display_completion_summary(str(result)[:200] if result else None)
    return result


# Convenience function for easy integration with existing main functions
async def run_with_tui_progress(
    agent,
    task: str,
    is_hierarchical: bool = True,
    show_progress: bool = True
) -> Any:
    """
    Universal function to run any agent with TUI progress display

    Args:
        agent: Agent to run (single or hierarchical)
        task: Task to execute
        is_hierarchical: Whether this is a hierarchical agent system
        show_progress: Whether to show progress display

    Returns:
        Agent execution result
    """
    if is_hierarchical:
        return await run_hierarchical_agent_with_progress(agent, task, show_progress)
    else:
        return await run_agent_with_progress(agent, task, show_progress)


if __name__ == "__main__":
    # Test integration with mock agent
    class MockAgent:
        def __init__(self, name: str):
            self.name = name

        async def run(self, task: str):
            # Simulate agent work
            for i in range(10):
                await asyncio.sleep(0.2)
            return f"Agent {self.name} completed task: {task}"

    async def test_integration():
        agent = MockAgent("Test Agent")
        result = await run_with_tui_progress(
            agent,
            "Test task for progress integration",
            is_hierarchical=False
        )
        print(f"Final result: {result}")

    asyncio.run(test_integration())