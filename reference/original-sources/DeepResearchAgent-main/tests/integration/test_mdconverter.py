import argparse
import warnings

warnings.simplefilter("ignore", DeprecationWarning)

from mmengine import DictAction

from src.config import config
from src.logger import logger
from src.models import model_manager
from src.tools.markdown.mdconvert import MarkitdownConverter
from src.utils import assemble_project_path


def parse_args():
    parser = argparse.ArgumentParser(description='main')
    parser.add_argument(
        "--config",
        default=assemble_project_path("configs/config_general.py"),
        help="config file path"
    )

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


if __name__ == "__main__":

    # Parse command line arguments
    args = parse_args()

    # Initialize the configuration
    config.init_config(args.config, args)

    # Initialize the logger
    logger.init_logger(log_path=config.log_path)
    logger.info(f"| Logger initialized at: {config.log_path}")
    logger.info(f"| Config:\n{config.pretty_text}")

    # Registered models
    model_manager.init_models(use_local_proxy=True)
    registered_models = ", ".join(model_manager.registered_models.keys())
    logger.info("Registered models: %s", registered_models)

    mdconvert = MarkitdownConverter()
    url = (
        "https://www.theguardian.com/food/2021/may/01/"
        "yotam-ottolenghis-recipes-for-takeaway-classics"
    )
    md = mdconvert.convert(url)
    print(md)
