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


def parse_args():
    parser = argparse.ArgumentParser(description='Interactive DeepResearchAgent TUI')
    parser.add_argument("--config", default=os.path.join(root, "configs", "config_main.py"), help="config file path")
    parser.add_argument("--task", type=str, help="Research task to execute")

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
    Main entry point for interactive DeepResearchAgent

    Args:
        task (str, optional): Research task to execute. If None, will use default demo task.
    """
    try:
        # Parse command line arguments
        args = parse_args()

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

    # Run the task
    res = await agent.run(task)
    logger.info(f"| Result: {res}")

    return res


if __name__ == '__main__':
    asyncio.run(main())