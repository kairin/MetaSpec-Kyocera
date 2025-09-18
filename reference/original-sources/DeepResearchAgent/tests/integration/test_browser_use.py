import warnings

warnings.simplefilter("ignore", DeprecationWarning)

import argparse
import asyncio

from dotenv import load_dotenv

load_dotenv(verbose=True)

from src.tools.auto_browser import AutoBrowserUseTool
from src.utils import assemble_project_path


def parse_args():
    parser = argparse.ArgumentParser(description='main')
    parser.add_argument(
        "--config",
        default=assemble_project_path("configs/config_general.py"),
        help="config file path"
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":

    tool = AutoBrowserUseTool()

    loop = asyncio.get_event_loop()

    # task1 = (
    #     "Find the minimum perigee value (closest approach distance) "
    #     "between the Earth and the Moon on the Wikipedia page for the Moon."
    # )
    # res = loop.run_until_complete(tool.forward(task=task1))
    # print(res)
    #
    # task2 = "Eliud Kipchoge's marathon world record time and pace"
    # res = loop.run_until_complete(tool.forward(task=task2))
    # print(res)

    task3 = (
        "Open the pdf https://arxiv.org/abs/2506.12508, then extract "
        "the first paragraph of the page 3."
    )
    res = loop.run_until_complete(tool.forward(task=task3))
    print(res)
