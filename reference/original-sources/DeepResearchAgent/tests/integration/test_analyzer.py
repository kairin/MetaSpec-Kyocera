import warnings

warnings.simplefilter("ignore", DeprecationWarning)

import argparse
import asyncio

from src.tools.deep_analyzer import DeepAnalyzerTool
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

    deep_analyzer = DeepAnalyzerTool()

    task = """
    Please give a detailed analysis of the following image.
    """

    response = asyncio.run(
        deep_analyzer.forward(
            task=task,
            source=assemble_project_path(
                "data/GAIA/2023/validation/"
                "b2c257e0-3ad7-4f05-b8e3-d9da973be36e.jpg"
            )
        )
    )

    print(response)
