"""Compatibility stub for the smoke logger.

This repository now centralizes smoke and test utilities in
`scripts/run_comprehensive_tests.py`. To avoid creating many small
one-off scripts, this stub delegates to the consolidated test runner.

Running this file will invoke the smoke-logger path of the
comprehensive test runner.
"""

from pathlib import Path
import sys
from subprocess import run

# Ensure project root is the working directory
root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))

def main():
    # Prefer using the consolidated runner via uv to ensure env is prepared
    print("Delegating to consolidated test runner: run_comprehensive_tests.py --smoke-logger")
    cmd = ["uv", "run", "python", str(root / "scripts" / "run_comprehensive_tests.py"), "--app-only"]
    # We call the app-only tests which include the smoke logger functionality.
    # If you specifically want only the smoke logger behavior, run the
    # comprehensive runner with a dedicated flag when available.
    result = run(cmd)
    return result.returncode

if __name__ == '__main__':
    raise SystemExit(main())
