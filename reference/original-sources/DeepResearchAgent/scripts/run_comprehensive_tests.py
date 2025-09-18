#!/usr/bin/env python3
"""
Comprehensive Test Runner for DeepResearchAgent

This script runs all tests with detailed logging and reporting.
It executes unit tests, integration tests, and provides comprehensive
debugging information for the DeepResearchAgent application.
"""

import argparse
import json
import logging
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# Add project root to path
root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
# Import the project's AgentLogger so we can run the smoke logger as part of the
# comprehensive test runner (consolidation of small test scripts).
try:
    from src.logger import logger
except Exception:
    logger = None


class TestRunner:
    """Comprehensive test runner for DeepResearchAgent."""

    def __init__(self, verbose: bool = False, log_level: str = "INFO",
                 coverage: bool = False):
        self.verbose = verbose
        self.log_level = log_level
        self.coverage = coverage
        self.test_results: dict = {}
        self.start_time = None
        self.end_time = None

        # Set up logging
        self.setup_logging()

    def setup_logging(self) -> None:
        """Set up comprehensive logging for testing with unique timestamps."""
        # Create test output directory
        self.test_output_dir = root / "test_output"
        self.test_output_dir.mkdir(exist_ok=True)

        # Create unique timestamp with microsecond precision and process ID
        # Format: YYYYMMDD_HHMMSS_microseconds_PID
        now = datetime.now()
        microseconds = now.microsecond
        pid = os.getpid()
        timestamp = f"{now.strftime('%Y%m%d_%H%M%S')}_{microseconds:06d}_{pid}"
        self.log_file = self.test_output_dir / f"test_run_{timestamp}.log"

        # Configure dedicated test logger (not root logger to avoid conflicts)
        self.test_logger = logging.getLogger(f"test_runner_{pid}")
        self.test_logger.setLevel(getattr(logging, self.log_level))

        # Remove any existing handlers to avoid duplicates
        for handler in self.test_logger.handlers[:]:
            self.test_logger.removeHandler(handler)

        # Create file handler with detailed formatting
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(getattr(logging, self.log_level))

        # Enhanced formatter with more details
        formatter = logging.Formatter(
            '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - '
            '[PID:%(process)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        self.test_logger.addHandler(file_handler)

        # Prevent log propagation to avoid duplicate messages
        self.test_logger.propagate = False

        # Log session start information
        self.test_logger.info("=" * 80)
        self.test_logger.info("TEST SESSION STARTED")
        self.test_logger.info(f"Timestamp: {now.isoformat()}")
        self.test_logger.info(f"Process ID: {pid}")
        self.test_logger.info(f"Python Version: {sys.version}")
        self.test_logger.info(f"Working Directory: {os.getcwd()}")
        self.test_logger.info(f"Log File: {self.log_file}")
        self.test_logger.info("=" * 80)

    def log_session_completion(self, results: dict) -> None:
        """Log test session completion with comprehensive results."""
        end_time = datetime.now()

        self.test_logger.info("=" * 80)
        self.test_logger.info("TEST SESSION COMPLETED")
        self.test_logger.info(f"End Timestamp: {end_time.isoformat()}")

        if "summary" in results:
            summary = results["summary"]
            self.test_logger.info("FINAL RESULTS SUMMARY:")
            self.test_logger.info(f"  Total Tests: {summary['total_tests']}")
            self.test_logger.info(f"  Passed: {summary['passed']}")
            self.test_logger.info(f"  Failed: {summary['failed']}")
            self.test_logger.info(f"  Errors: {summary['errors']}")
            self.test_logger.info(f"  Duration: {summary['duration']:.2f}s")

        if "total_duration" in results:
            self.test_logger.info(
                f"Total Session Duration: {results['total_duration']:.2f}s"
            )

        self.test_logger.info("=" * 80)

    def run_command(self, cmd: list[str], description: str,
                    cwd: Path | None = None) -> dict:
        """Run a command and capture comprehensive output."""
        print(f"🚀 Running: {description}")
        if self.verbose:
            print(f"   Command: {' '.join(cmd)}")

        # Log command start
        self.test_logger.info(f"Starting command: {description}")
        self.test_logger.info(f"Command: {' '.join(cmd)}")
        if cwd:
            self.test_logger.info(f"Working directory: {cwd}")

        start_time = time.time()
        result = subprocess.run(
            cmd,
            cwd=cwd or root,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONPATH": str(root)}
        )
        end_time = time.time()

        output = {
            "command": " ".join(cmd),
            "description": description,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "duration": end_time - start_time,
            "success": result.returncode == 0
        }

        # Comprehensive logging of results
        self.test_logger.info(f"Command completed: {description}")
        self.test_logger.info(f"Return code: {result.returncode}")
        self.test_logger.info(f"Duration: {output['duration']:.2f}s")
        self.test_logger.info(f"Success: {output['success']}")

        if result.stdout:
            # Log stdout with clear markers for different output types
            if "pytest" in cmd[0] or any("pytest" in arg for arg in cmd):
                self.test_logger.info("PYTEST STDOUT:")
            else:
                self.test_logger.info("COMMAND STDOUT:")
            # Split stdout into lines for better log readability
            for line in result.stdout.splitlines():
                self.test_logger.info(f"  {line}")

        if result.stderr:
            self.test_logger.warning("COMMAND STDERR:")
            # Split stderr into lines for better log readability
            for line in result.stderr.splitlines():
                self.test_logger.warning(f"  {line}")

        return output

    def run_unit_tests(self) -> dict:
        """Run unit tests."""
        self.test_logger.info("STARTING UNIT TESTS PHASE")
        print("\n🧪 Running Unit Tests...")
        cmd = [
            sys.executable, "-m", "pytest",
            str(root / "tests" / "unit"),
            "-v",
            "--tb=short",
            "--durations=10",
            "--strict-markers",
            "-m", "unit"
        ]

        if self.coverage:
            cmd.extend([
                "--cov=src",
                "--cov-report=xml:test_output/coverage.xml",
                "--cov-report=html:test_output/coverage_html",
                "--cov-report=term-missing"
            ])

        if not self.verbose:
            cmd.extend(["--quiet"])

        result = self.run_command(cmd, "Unit Tests")
        self.test_logger.info("UNIT TESTS PHASE COMPLETED")
        return result

    def run_integration_tests(self) -> dict:
        """Run integration tests."""
        self.test_logger.info("STARTING INTEGRATION TESTS PHASE")
        print("\n🔗 Running Integration Tests...")
        results = {}

        # Run each integration test script
        integration_dir = root / "tests" / "integration"
        for test_file in integration_dir.glob("test_*.py"):
            self.test_logger.info(
                f"Running integration test: {test_file.name}"
            )
            print(f"   Running {test_file.name}...")
            # Use uv run to ensure virtual environment is activated
            cmd = ["uv", "run", "python", str(test_file)]
            result = self.run_command(
                cmd, f"Integration Test: {test_file.name}")
            results[test_file.name] = result

        self.test_logger.info("INTEGRATION TESTS PHASE COMPLETED")
        return results

    def run_app_tests(self) -> dict:
        """Run application with comprehensive logging."""
        self.test_logger.info("STARTING APPLICATION TESTS PHASE")
        print("\n🚀 Running Application Tests...")

        results = {}

        # Test 1: Basic app startup
        self.test_logger.info("Running application startup test")
        print("   Testing basic app startup...")
        cmd = ["uv", "run", "python", str(root / "main.py"), "--help"]
        results["app_help"] = self.run_command(cmd, "App Help Command")

        # Test 2: Config validation
        self.test_logger.info("Running configuration validation test")
        print("   Testing config validation...")
        cmd = [
            "uv", "run", "python",
            str(root / "tests" / "integration" / "test_config.py")
        ]
        results["config_test"] = self.run_command(cmd, "Config Test")

        # Test 3: TUI mode (test launch with timeout)
        print("   Testing TUI mode...")
        cmd = ["timeout", "5", "uv", "run", "python", "main.py", "--tui"]
        result = self.run_command(cmd, "TUI Launch Test")
        # For TUI test, timeout (124) is expected and considered success
        if result["returncode"] == 124:
            result["success"] = True
            result["description"] += " (timeout expected)"
        results["tui_test"] = result

        self.test_logger.info("APPLICATION TESTS PHASE COMPLETED")
        return results

    def run_smoke_logger(self) -> dict:
        """Run a lightweight smoke test that exercises the project's AgentLogger.

        This consolidates the behavior previously provided by
        `scripts/smoke_logger.py` into this single test runner.
        """
        self.test_logger.info("STARTING SMOKE LOGGER TEST")
        print("🔍 Running smoke logger test...")

        # Ensure outputs/logs exists
        log_dir = root / "outputs" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        smoke_log = log_dir / "smoke_from_test_runner.log"

        if logger is None:
            msg = "Project logger could not be imported; smoke logger skipped."
            self.test_logger.warning(msg)
            return {"success": False, "stderr": msg, "returncode": 1}

        try:
            # Initialize project logger to write to the smoke log file
            logger.init_logger(log_path=str(smoke_log))
            logger.log_rule('Smoke logger test (from comprehensive runner)')
            logger.info('Info message from comprehensive test runner smoke test')
            logger.debug('Debug message from comprehensive test runner smoke test')
            logger.log_code('Example code', 'print("hello smoke")')
            logger.log_markdown('# Sample\nThis is a markdown log entry (runner).', title='MD Test')
            self.test_logger.info(f"Smoke logger wrote to: {smoke_log}")
            return {"success": True, "returncode": 0, "stdout": f"Wrote {smoke_log}"}
        except Exception as e:
            self.test_logger.error(f"Smoke logger test failed: {e}")
            return {"success": False, "returncode": 1, "stderr": str(e)}

    def run_comprehensive_test(self) -> dict:
        """Run comprehensive test suite."""
        print("🧪 Starting Comprehensive Test Suite")
        print("=" * 50)

        self.start_time = time.time()
        results = {}

        try:
            # Run unit tests
            results["unit_tests"] = self.run_unit_tests()

            # Run integration tests
            results["integration_tests"] = self.run_integration_tests()

            # Run app tests
            results["app_tests"] = self.run_app_tests()

            # Generate summary
            results["summary"] = self.generate_summary(results)

        except Exception as e:
            self.test_logger.error(f"Test suite failed with error: {e}")
            results["error"] = str(e)

        finally:
            self.end_time = time.time()
            results["total_duration"] = self.end_time - self.start_time

        return results

    def generate_summary(self, results: dict) -> dict:
        """Generate test summary."""
        summary = {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "duration": (
                (self.end_time - self.start_time)
                if self.end_time is not None and self.start_time is not None
                else 0
            )
        }

        def analyze_result(result):
            if isinstance(result, dict):
                if "success" in result:
                    summary["total_tests"] += 1
                    if result["success"]:
                        summary["passed"] += 1
                    else:
                        summary["failed"] += 1
                elif "returncode" in result:
                    summary["total_tests"] += 1
                    if result["returncode"] == 0:
                        summary["passed"] += 1
                    else:
                        summary["failed"] += 1
                else:
                    # Recursively analyze nested results
                    for key, value in result.items():
                        if key != "summary":
                            analyze_result(value)

        analyze_result(results)
        return summary

    def print_results(self, results: dict) -> None:
        """Print test results to console."""
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)

        if "summary" in results:
            summary = results["summary"]
            print(f"Total Tests: {summary['total_tests']}")
            print(f"Passed: {summary['passed']}")
            print(f"Failed: {summary['failed']}")
            print(".2f")
            print(".2f")

        print(f"\n📝 Detailed log saved to: {self.log_file}")

        # Print failures
        print("\n❌ FAILED TESTS:")

        def print_failures(result, prefix="") -> None:
            if isinstance(result, dict):
                for key, value in result.items():
                    if key == "summary":
                        continue
                    if isinstance(value, dict):
                        if "success" in value and not value["success"]:
                            print(f"  {prefix}{key}: FAILED")
                            if "stderr" in value and value["stderr"]:
                                print(f"    Error: {value['stderr'][:200]}...")
                        elif ("returncode" in value and
                              value["returncode"] != 0):
                            print(f"  {prefix}{key}: FAILED "
                                  f"(code {value['returncode']})")
                            if "stderr" in value and value["stderr"]:
                                print(f"    Error: {value['stderr'][:200]}...")
                        else:
                            print_failures(value, f"{prefix}{key}.")

        print_failures(results)

        print("\n✅ PASSED TESTS:")

        def print_successes(result, prefix="") -> None:
            if isinstance(result, dict):
                for key, value in result.items():
                    if key == "summary":
                        continue
                    if isinstance(value, dict):
                        if "success" in value and value["success"]:
                            print(f"  {prefix}{key}: PASSED")
                        elif ("returncode" in value and
                              value["returncode"] == 0):
                            print(f"  {prefix}{key}: PASSED")
                        else:
                            print_successes(value, f"{prefix}{key}.")

        print_successes(results)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Comprehensive Test Runner")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Enable verbose output")
    parser.add_argument("--log-level", default="INFO",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                        help="Logging level")
    parser.add_argument("--unit-only", action="store_true",
                        help="Run only unit tests")
    parser.add_argument("--integration-only", action="store_true",
                        help="Run only integration tests")
    parser.add_argument("--app-only", action="store_true",
                        help="Run only app tests")
    parser.add_argument("--coverage", action="store_true",
                        help="Generate coverage reports")

    args = parser.parse_args()

    # Initialize test runner
    runner = TestRunner(verbose=args.verbose, log_level=args.log_level,
                        coverage=args.coverage)

    try:
        if args.unit_only:
            results = {"unit_tests": runner.run_unit_tests()}
        elif args.integration_only:
            results = {"integration_tests": runner.run_integration_tests()}
        elif args.app_only:
            results = {"app_tests": runner.run_app_tests()}
        else:
            results = runner.run_comprehensive_test()

        runner.print_results(results)

        # Log session completion
        runner.log_session_completion(results)

        # Save results to JSON with unique timestamp
        now = datetime.now()
        microseconds = now.microsecond
        pid = os.getpid()
        timestamp = f"{now.strftime('%Y%m%d_%H%M%S')}_{microseconds:06d}_{pid}"
        results_file = (runner.test_output_dir /
                        f"test_results_{timestamp}.json")
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n💾 Results saved to: {results_file}")

        # Also save a copy to the fixed filename for backwards compatibility
        fixed_results_file = runner.test_output_dir / "test_results.json"
        with open(fixed_results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"💾 Also saved to: {fixed_results_file} (latest results)")

        # Exit with appropriate code
        if "summary" in results and results["summary"]["failed"] > 0:
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n⏹️  Test run interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test runner failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
