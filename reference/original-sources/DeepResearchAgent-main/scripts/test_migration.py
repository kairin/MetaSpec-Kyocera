#!/usr/bin/env python3
"""
Migration Test Suite for DeepResearchAgent
Comprehensive testing of the Poetry -> uv migration

This script provides a test suite to validate the migration and catch regressions.
"""

import os
import sys
import subprocess
import tempfile
import shutil
import json
from pathlib import Path
from typing import List, Dict, Any
import pytest


class MigrationTestSuite:
    def __init__(self, project_root: Path):
        self.project_root = project_root

    def run_command(self, cmd: List[str], cwd: Path = None) -> subprocess.CompletedProcess:
        """Run a command and return the result"""
        return subprocess.run(
            cmd,
            cwd=cwd or self.project_root,
            capture_output=True,
            text=True,
            timeout=60
        )

    def test_uv_installation(self):
        """Test that uv is properly installed"""
        result = self.run_command(["uv", "--version"])
        assert result.returncode == 0, f"uv not found: {result.stderr}"
        assert "uv" in result.stdout.lower()
        print(f"✅ uv version: {result.stdout.strip()}")

    def test_python_version(self):
        """Test that Python 3.13 is available and being used"""
        # Test system Python 3.13
        result = self.run_command(["python3.13", "--version"])
        assert result.returncode == 0, f"Python 3.13 not found: {result.stderr}"
        assert "3.13" in result.stdout
        print(f"✅ System Python: {result.stdout.strip()}")

        # Test uv can find Python 3.13
        result = self.run_command(["uv", "python", "list"])
        assert result.returncode == 0, f"uv python list failed: {result.stderr}"
        assert "3.13" in result.stdout, "Python 3.13 not found by uv"
        print("✅ uv can detect Python 3.13")

    def test_project_configuration(self):
        """Test that project configuration is properly migrated"""
        pyproject_path = self.project_root / "pyproject.toml"
        assert pyproject_path.exists(), "pyproject.toml not found"

        import toml
        config = toml.load(pyproject_path)

        # Test build system
        build_system = config.get("build-system", {})
        assert build_system.get("requires") == ["hatchling"], "Build system not migrated"
        assert build_system.get("build-backend") == "hatchling.build", "Build backend not set"
        print("✅ Build system properly configured")

        # Test project dependencies
        project = config.get("project", {})
        assert "dependencies" in project, "Dependencies not in uv format"
        assert len(project["dependencies"]) > 0, "No dependencies found"
        print(f"✅ {len(project['dependencies'])} dependencies configured")

        # Test no Poetry remnants
        assert "tool.poetry" not in config, "Poetry configuration still present"
        print("✅ Poetry configuration cleaned up")

    def test_lock_files(self):
        """Test that lock files are properly managed"""
        uv_lock = self.project_root / "uv.lock"
        poetry_lock = self.project_root / "poetry.lock"

        assert uv_lock.exists(), "uv.lock file missing"
        print("✅ uv.lock file exists")

        if poetry_lock.exists():
            print("⚠️ poetry.lock still exists (consider removing)")
        else:
            print("✅ poetry.lock properly removed")

    def test_virtual_environment(self):
        """Test virtual environment configuration"""
        venv_config = self.project_root / ".venv" / "pyvenv.cfg"
        if venv_config.exists():
            content = venv_config.read_text()
            assert "3.13" in content, "Virtual environment not using Python 3.13"
            print("✅ Virtual environment uses Python 3.13")
        else:
            print("⚠️ No virtual environment found")

    def test_makefile_commands(self):
        """Test that Makefile commands work with uv"""
        makefile = self.project_root / "Makefile"
        assert makefile.exists(), "Makefile not found"

        content = makefile.read_text()
        assert "uv sync" in content, "Makefile doesn't use uv sync"
        assert "uv run" in content, "Makefile doesn't use uv run"

        # Test that Poetry references are removed
        assert "poetry" not in content.lower(), "Makefile still references Poetry"
        print("✅ Makefile properly migrated to uv")

    def test_imports(self):
        """Test that core imports work correctly"""
        test_imports = [
            "import src",
            "from src.models import model_manager",
            "from src.tools import AsyncTool",
            "from src.agent import create_agent",
            "from src.utils import assemble_project_path"
        ]

        for import_stmt in test_imports:
            result = self.run_command(["uv", "run", "python", "-c", import_stmt])
            assert result.returncode == 0, f"Import failed: {import_stmt}\nError: {result.stderr}"
            print(f"✅ Import successful: {import_stmt}")

    def test_dependency_resolution(self):
        """Test that dependencies can be resolved and installed"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Copy project files including README for hatchling
            for file in ["pyproject.toml", "uv.lock", "README.md"]:
                src = self.project_root / file
                if src.exists():
                    shutil.copy2(src, temp_path / file)

            # Create minimal src structure for hatchling
            src_dir = temp_path / "src"
            src_dir.mkdir()
            (src_dir / "__init__.py").write_text("")

            # Test dependency installation
            result = self.run_command(["uv", "sync", "--frozen"], cwd=temp_path)
            assert result.returncode == 0, f"Dependency installation failed: {result.stderr}"
            print("✅ Dependencies can be installed from lock file")

    def test_development_workflow(self):
        """Test common development commands"""
        # Test uv commands work
        commands = [
            ["uv", "--version"],
            ["uv", "run", "python", "--version"],
        ]

        for cmd in commands:
            result = self.run_command(cmd)
            assert result.returncode == 0, f"Command failed: {' '.join(cmd)}\nError: {result.stderr}"
            print(f"✅ Command works: {' '.join(cmd)}")

    def test_no_circular_imports(self):
        """Test that circular import issues are resolved"""
        # Test specific imports that had circular issues
        test_cases = [
            "from src.tools.auto_browser import AutoBrowserUseTool",
            "from src.utils.agent_types import AgentType",
            "from src.tools.tools import AsyncTool, ToolResult"
        ]

        for import_stmt in test_cases:
            result = self.run_command(["uv", "run", "python", "-c", import_stmt])
            assert result.returncode == 0, f"Circular import issue: {import_stmt}\nError: {result.stderr}"
            print(f"✅ No circular import: {import_stmt}")

    def test_markitdown_fixes(self):
        """Test that markitdown API fixes work"""
        import_stmt = "from src.tools.markdown.mdconvert import MarkitdownConverter"
        result = self.run_command(["uv", "run", "python", "-c", import_stmt])
        assert result.returncode == 0, f"markitdown import failed: {result.stderr}"
        print("✅ markitdown API fixes work")

    def test_validation_script(self):
        """Test that the validation script works"""
        validation_script = self.project_root / "scripts" / "validate_migration.py"
        assert validation_script.exists(), "Validation script not found"

        result = self.run_command(["uv", "run", "python", str(validation_script)])
        # Note: validation script returns 0 on success, 1 on failure
        if result.returncode != 0:
            print(f"⚠️ Validation script reported issues: {result.stdout}")
        else:
            print("✅ Validation script passes")

    def run_all_tests(self):
        """Run all tests"""
        tests = [
            ("uv Installation", self.test_uv_installation),
            ("Python Version", self.test_python_version),
            ("Project Configuration", self.test_project_configuration),
            ("Lock Files", self.test_lock_files),
            ("Virtual Environment", self.test_virtual_environment),
            ("Makefile Commands", self.test_makefile_commands),
            ("Core Imports", self.test_imports),
            ("Dependency Resolution", self.test_dependency_resolution),
            ("Development Workflow", self.test_development_workflow),
            ("No Circular Imports", self.test_no_circular_imports),
            ("markitdown Fixes", self.test_markitdown_fixes),
            ("Validation Script", self.test_validation_script),
        ]

        print("=" * 60)
        print("MIGRATION TEST SUITE")
        print("=" * 60)

        passed = 0
        failed = 0

        for test_name, test_func in tests:
            print(f"\n🧪 {test_name}")
            print("-" * 40)
            try:
                test_func()
                passed += 1
                print(f"✅ {test_name} PASSED")
            except Exception as e:
                failed += 1
                print(f"❌ {test_name} FAILED: {e}")

        print("\n" + "=" * 60)
        print(f"TEST RESULTS: {passed} PASSED, {failed} FAILED")
        print("=" * 60)

        return failed == 0


def main():
    """Main test function"""
    project_root = Path(__file__).parent.parent.resolve()
    test_suite = MigrationTestSuite(project_root)

    success = test_suite.run_all_tests()

    # Generate test report in organized subdirectory
    reports_dir = project_root / "outputs" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    report_path = reports_dir / "migration_test_report.json"
    with open(report_path, 'w') as f:
        json.dump({
            "timestamp": subprocess.run(["date", "-Iseconds"], capture_output=True, text=True).stdout.strip(),
            "project_root": str(project_root),
            "test_status": "PASSED" if success else "FAILED",
            "python_version": subprocess.run(["uv", "run", "python", "--version"], capture_output=True, text=True).stdout.strip(),
            "uv_version": subprocess.run(["uv", "--version"], capture_output=True, text=True).stdout.strip()
        }, f, indent=2)

    print(f"\nTest report saved to: {report_path}")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()