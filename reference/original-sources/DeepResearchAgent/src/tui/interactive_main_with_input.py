import argparse
import asyncio
import os
import sys
from pathlib import Path

from mmengine import DictAction

root = str(Path(__file__).resolve().parents[2])
sys.path.append(root)

# Apply compatibility fixes early
from src.compat import compatibility_manager
compatibility_manager.apply_compatibility_fixes()

from src.agent import create_agent
from src.config import config
from src.logger import logger
from src.models import model_manager
from src.tui.task_collector import get_user_task
from src.tui.agent_integration import run_with_tui_progress


def parse_args():
    parser = argparse.ArgumentParser(description='Interactive DeepResearchAgent TUI with Task Input')
    parser.add_argument("--config", default=os.path.join(root, "configs", "config_main.py"), help="config file path")
    parser.add_argument("--task", type=str, help="Research task to execute (skip interactive input)")
    parser.add_argument("--interactive", action="store_true", help="Enable interactive task input")
    parser.add_argument("--no-progress", action="store_true", help="Disable progress display (use logs only)")

    parser.add_argument(
        '--cfg-options',
        nargs='+',
        action=DictAction,
        help='override some settings in the used config, the key-value pair '
        'in xxx=yyy format will be merged into config file. If the value to '
        'be overwritten is a list, it should be like key="[a,b]" or key=a,b '
        'It also allows nested list/tuple values, e.g. key="[(a,b),(c,d)]" '
        'Note that the quotation marks are necessary and that no white space '
        'is allowed.')
    args = parser.parse_args()
    return args


async def main(task: str = None):
    """
    Main entry point for interactive DeepResearchAgent with task collection

    Args:
        task (str, optional): Research task to execute. If None, will collect from user interactively.
    """
    try:
        # Parse command line arguments
        args = parse_args()

        # Get task from interactive input if requested and no task provided
        if task is None and args.task is None and args.interactive:
            try:
                task = get_user_task()
            except KeyboardInterrupt:
                logger.info("| Task input cancelled by user")
                return
            except Exception as e:
                logger.error(f"| Error collecting task: {e}")
                return

        # Initialize the configuration
        config.init_config(args.config, args)

        # Initialize the logger
        logger.init_logger(log_path=config.log_path)
        logger.info(f"| Logger initialized at: {config.log_path}")
        logger.info(f"| Config:\n{config.pretty_text}")

        # Initialize models with validation
        logger.info("| Initializing models...")
        model_manager.init_models(use_local_proxy=True)
        logger.info("| Registered models: %s", ", ".join(model_manager.registered_models.keys()))

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
        task = "Use deep_researcher_agent to search the latest papers on the topic of 'AI Agent' and then summarize it."
        logger.info("| Using default demo task (no custom task provided)")
    else:
        logger.info(f"| Executing custom task: {task[:100]}...")

    # Determine if we should show progress display
    show_progress = not getattr(args, 'no_progress', False)

    if show_progress:
        # Run with TUI progress display
        logger.info(f"| Starting task execution with progress display...")
        res = await run_with_tui_progress(
            agent,
            task,
            is_hierarchical=True,
            show_progress=True
        )
    else:
        # Run without progress display (traditional logging)
        logger.info(f"| Starting task execution (logs only)...")
        res = await agent.run(task)

    logger.info(f"| Result: {res}")
    return res


if __name__ == '__main__':
    asyncio.run(main())