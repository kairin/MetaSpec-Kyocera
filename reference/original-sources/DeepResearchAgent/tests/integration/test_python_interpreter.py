import warnings

warnings.simplefilter("ignore", DeprecationWarning)

import argparse
import asyncio

from src.tools.python_interpreter import PythonInterpreterTool
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

    pit = PythonInterpreterTool()
    code = """
def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    else:
        fib_sequence = [0, 1]
        for i in range(2, n):
            fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
        return fib_sequence
result = fibonacci(10)
    """
    content = asyncio.run(pit.forward(code))
    print(content)

    # Validate the output
    expected_fibonacci = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    expected_output = f"Output: {expected_fibonacci}"
    if content.output is None or expected_output not in content.output:
        print("ERROR: Expected fibonacci sequence not found")
        exit(1)

    print("SUCCESS: Fibonacci sequence validation passed")
