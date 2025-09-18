#!/usr/bin/env python3
"""
Migration Validation Script for DeepResearchAgent
Validates the Poetry -> uv migration and Python 3.13 upgrade

This script performs comprehensive validation without hardcoded messages.
"""

import os
import subprocess
import sys
import json
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class ValidationResult:
    def __init__(self):
        self.checks = []
        self.passed = 0
        self.failed = 0
        self.warnings = 0

    def add_check(self, name: str, status: str, message: str, details: Optional[str] = None):
        """Add a validation check result"""
        self.checks.append({
            "name": name,
            "status": status,  # "PASS", "FAIL", "WARN"
            "message": message,
            "details": details
        })
        if status == "PASS":
            self.passed += 1
        elif status == "FAIL":
            self.failed += 1
        elif status == "WARN":
            self.warnings += 1

    def print_results(self):
        """Print validation results"""
        print(f"\n{'='*60}")
        print("MIGRATION VALIDATION RESULTS")
        print(f"{'='*60}")

        for check in self.checks:
            status_symbol = {
                "PASS": "✅",
                "FAIL": "❌",
                "WARN": "⚠️"
            }.get(check["status"], "❓")

            print(f"{status_symbol} {check['name']}: {check['message']}")
            if check["details"]:
                print(f"   Details: {check['details']}")

        print(f"\n{'='*60}")
        print(f"SUMMARY: {self.passed} PASSED, {self.failed} FAILED, {self.warnings} WARNINGS")
        print(f"{'='*60}\n")

        return self.failed == 0


class MigrationValidator:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.result = ValidationResult()

    def run_command(self, cmd: List[str], cwd: Optional[Path] = None) -> Tuple[int, str, str]:
        """Run a command and return (returncode, stdout, stderr)"""
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd or self.project_root,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out"
        except Exception as e:
            return -1, "", str(e)

    def validate_python_version(self):
        """Validate Python 3.13 is being used"""
        # Check system Python 3.13
        returncode, stdout, stderr = self.run_command(["python3.13", "--version"])
        if returncode == 0 and "3.13" in stdout:
            self.result.add_check(
                "System Python 3.13",
                "PASS",
                f"System Python 3.13 available: {stdout.strip()}"
            )
        else:
            self.result.add_check(
                "System Python 3.13",
                "FAIL",
                "Python 3.13 not found on system",
                f"stdout: {stdout}, stderr: {stderr}"
            )

        # Check uv Python configuration
        returncode, stdout, stderr = self.run_command(["uv", "python", "list"])
        if returncode == 0:
            if "3.13" in stdout:
                self.result.add_check(
                    "uv Python 3.13 Detection",
                    "PASS",
                    "uv can detect Python 3.13"
                )
            else:
                self.result.add_check(
                    "uv Python 3.13 Detection",
                    "WARN",
                    "Python 3.13 not found in uv python list"
                )
        else:
            self.result.add_check(
                "uv Python Detection",
                "FAIL",
                "Failed to run 'uv python list'",
                stderr
            )

    def validate_virtual_environment(self):
        """Validate virtual environment uses Python 3.13"""
        venv_config = self.project_root / ".venv" / "pyvenv.cfg"
        if venv_config.exists():
            try:
                content = venv_config.read_text()
                if "3.13" in content:
                    self.result.add_check(
                        "Virtual Environment Python Version",
                        "PASS",
                        "Virtual environment uses Python 3.13"
                    )
                else:
                    self.result.add_check(
                        "Virtual Environment Python Version",
                        "FAIL",
                        "Virtual environment not using Python 3.13",
                        content
                    )
            except Exception as e:
                self.result.add_check(
                    "Virtual Environment Config",
                    "FAIL",
                    "Could not read pyvenv.cfg",
                    str(e)
                )
        else:
            self.result.add_check(
                "Virtual Environment",
                "WARN",
                "No virtual environment found at .venv/"
            )

    def validate_uv_installation(self):
        """Validate uv is properly installed and working"""
        returncode, stdout, stderr = self.run_command(["uv", "--version"])
        if returncode == 0:
            self.result.add_check(
                "uv Installation",
                "PASS",
                f"uv installed: {stdout.strip()}"
            )
        else:
            self.result.add_check(
                "uv Installation",
                "FAIL",
                "uv not found or not working",
                stderr
            )

    def validate_pyproject_toml(self):
        """Validate pyproject.toml has been migrated from Poetry to uv"""
        pyproject_path = self.project_root / "pyproject.toml"
        if pyproject_path.exists():
            try:
                import toml
                config = toml.load(pyproject_path)

                # Check build system
                build_system = config.get("build-system", {})
                if build_system.get("requires") == ["hatchling"]:
                    self.result.add_check(
                        "Build System Migration",
                        "PASS",
                        "Build system migrated to hatchling"
                    )
                else:
                    self.result.add_check(
                        "Build System Migration",
                        "FAIL",
                        "Build system not properly migrated",
                        f"Current: {build_system}"
                    )

                # Check for Poetry sections (should be gone)
                if "tool.poetry" in config:
                    self.result.add_check(
                        "Poetry Cleanup",
                        "FAIL",
                        "Poetry configuration still present in pyproject.toml"
                    )
                else:
                    self.result.add_check(
                        "Poetry Cleanup",
                        "PASS",
                        "Poetry configuration removed from pyproject.toml"
                    )

                # Check for dependencies section
                if "dependencies" in config.get("project", {}):
                    self.result.add_check(
                        "Dependencies Format",
                        "PASS",
                        "Dependencies in uv format (project.dependencies)"
                    )
                else:
                    self.result.add_check(
                        "Dependencies Format",
                        "FAIL",
                        "Dependencies not in uv format"
                    )

            except Exception as e:
                self.result.add_check(
                    "pyproject.toml Validation",
                    "FAIL",
                    "Could not parse pyproject.toml",
                    str(e)
                )
        else:
            self.result.add_check(
                "pyproject.toml Exists",
                "FAIL",
                "pyproject.toml not found"
            )

    def validate_lock_files(self):
        """Validate correct lock files exist"""
        uv_lock = self.project_root / "uv.lock"
        poetry_lock = self.project_root / "poetry.lock"

        if uv_lock.exists():
            self.result.add_check(
                "uv.lock File",
                "PASS",
                "uv.lock file exists"
            )
        else:
            self.result.add_check(
                "uv.lock File",
                "FAIL",
                "uv.lock file missing"
            )

        if poetry_lock.exists():
            self.result.add_check(
                "Poetry Lock Cleanup",
                "WARN",
                "poetry.lock still exists (should be removed)"
            )
        else:
            self.result.add_check(
                "Poetry Lock Cleanup",
                "PASS",
                "poetry.lock properly removed"
            )

    def validate_makefile(self):
        """Validate Makefile uses uv commands"""
        makefile_path = self.project_root / "Makefile"
        if makefile_path.exists():
            try:
                content = makefile_path.read_text()

                # Check for uv usage
                if "uv sync" in content and "uv run" in content:
                    self.result.add_check(
                        "Makefile uv Integration",
                        "PASS",
                        "Makefile uses uv commands"
                    )
                else:
                    self.result.add_check(
                        "Makefile uv Integration",
                        "FAIL",
                        "Makefile doesn't use uv commands"
                    )

                # Check for Poetry references (should be gone)
                if "poetry" in content.lower():
                    self.result.add_check(
                        "Makefile Poetry Cleanup",
                        "WARN",
                        "Makefile still references Poetry"
                    )
                else:
                    self.result.add_check(
                        "Makefile Poetry Cleanup",
                        "PASS",
                        "Poetry references removed from Makefile"
                    )

            except Exception as e:
                self.result.add_check(
                    "Makefile Validation",
                    "FAIL",
                    "Could not read Makefile",
                    str(e)
                )
        else:
            self.result.add_check(
                "Makefile Exists",
                "WARN",
                "Makefile not found"
            )

    def validate_imports(self):
        """Validate core imports work"""
        test_imports = [
            "import src",
            "from src.models import model_manager",
            "from src.tools import AsyncTool",
            "from src.agent import create_agent"
        ]

        for import_stmt in test_imports:
            returncode, stdout, stderr = self.run_command([
                "uv", "run", "python", "-c", import_stmt
            ])

            if returncode == 0:
                self.result.add_check(
                    f"Import: {import_stmt}",
                    "PASS",
                    "Import successful"
                )
            else:
                self.result.add_check(
                    f"Import: {import_stmt}",
                    "FAIL",
                    "Import failed",
                    stderr
                )

    def search_legacy_references(self):
        """Search for any remaining pip/poetry references"""
        search_patterns = ["pip install", "poetry", "conda install", "pipenv"]
        legacy_found = []

        # Search in Python files
        for pattern in search_patterns:
            returncode, stdout, stderr = self.run_command([
                "grep", "-r", "--include=*.py", "--include=*.md",
                "--include=*.txt", "--include=*.yml", "--include=*.yaml",
                pattern, "."
            ])

            if returncode == 0 and stdout.strip():
                legacy_found.append(f"{pattern}: {len(stdout.splitlines())} occurrences")

        if legacy_found:
            self.result.add_check(
                "Legacy Package Manager References",
                "WARN",
                "Found legacy references",
                "; ".join(legacy_found)
            )
        else:
            self.result.add_check(
                "Legacy Package Manager References",
                "PASS",
                "No legacy package manager references found"
            )

    def test_clean_environment_creation(self):
        """Test creating a fresh environment"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Copy essential files
            for file in ["pyproject.toml", "uv.lock"]:
                src = self.project_root / file
                if src.exists():
                    shutil.copy2(src, temp_path / file)

            # Try to create fresh environment
            returncode, stdout, stderr = self.run_command([
                "uv", "venv", ".venv", "--python", "3.13"
            ], cwd=temp_path)

            if returncode == 0:
                self.result.add_check(
                    "Clean Environment Creation",
                    "PASS",
                    "Can create fresh uv environment with Python 3.13"
                )
            else:
                self.result.add_check(
                    "Clean Environment Creation",
                    "FAIL",
                    "Failed to create fresh uv environment",
                    stderr
                )

    def run_all_validations(self):
        """Run all validation checks"""
        print("Starting migration validation...")

        self.validate_uv_installation()
        self.validate_python_version()
        self.validate_virtual_environment()
        self.validate_pyproject_toml()
        self.validate_lock_files()
        self.validate_makefile()
        self.validate_imports()
        self.search_legacy_references()
        self.test_clean_environment_creation()

        return self.result.print_results()


def main():
    """Main validation function"""
    project_root = Path(__file__).parent.parent.resolve()
    validator = MigrationValidator(project_root)

    success = validator.run_all_validations()

    # Generate JSON report in organized subdirectory
    reports_dir = project_root / "outputs" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    report_path = reports_dir / "migration_validation_report.json"
    with open(report_path, 'w') as f:
        json.dump({
            "timestamp": subprocess.run(["date", "-Iseconds"], capture_output=True, text=True).stdout.strip(),
            "project_root": str(project_root),
            "results": validator.result.checks,
            "summary": {
                "passed": validator.result.passed,
                "failed": validator.result.failed,
                "warnings": validator.result.warnings,
                "success": success
            }
        }, f, indent=2)

    print(f"Detailed report saved to: {report_path}")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()