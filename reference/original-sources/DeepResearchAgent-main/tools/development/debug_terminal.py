#!/usr/bin/env python3
"""Debug terminal capabilities for Textual."""

import sys
import os
from textual import __version__ as textual_version

def debug_terminal():
    """Debug terminal capabilities."""
    print(f"🔍 Terminal Debug Information")
    print(f"Python version: {sys.version}")
    print(f"Textual version: {textual_version}")
    print()

    print("📱 Terminal Environment:")
    print(f"  TERM: {os.environ.get('TERM', 'Not set')}")
    print(f"  COLORTERM: {os.environ.get('COLORTERM', 'Not set')}")
    print(f"  TERMINAL_EMULATOR: {os.environ.get('TERMINAL_EMULATOR', 'Not set')}")
    print()

    print("🖥️  Terminal Capabilities:")
    print(f"  stdin.isatty(): {sys.stdin.isatty()}")
    print(f"  stdout.isatty(): {sys.stdout.isatty()}")
    print(f"  stderr.isatty(): {sys.stderr.isatty()}")
    print()

    # Try to get terminal size
    try:
        import shutil
        cols, rows = shutil.get_terminal_size()
        print(f"  Terminal size: {cols}x{rows}")
    except Exception as e:
        print(f"  Terminal size: Error getting size - {e}")

    print()
    print("🚀 Testing basic escape sequences:")

    # Test basic ANSI escape sequences
    print("  Testing colors: \033[31mRED\033[0m \033[32mGREEN\033[0m \033[34mBLUE\033[0m")
    print("  Testing cursor movement: ", end="")
    sys.stdout.write("\033[5C")  # Move cursor right 5 positions
    print("MOVED")

    print()
    print("🔧 Environment test for Textual compatibility:")

    # Check if running in a proper terminal
    if sys.stdin.isatty() and sys.stdout.isatty():
        print("  ✅ Running in interactive terminal")
    else:
        print("  ❌ Not running in interactive terminal")

    # Test terminal capabilities
    try:
        import subprocess
        result = subprocess.run(['tput', 'colors'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  Terminal colors: {result.stdout.strip()}")
        else:
            print("  Terminal colors: Unknown")
    except Exception:
        print("  Terminal colors: Could not detect")

if __name__ == "__main__":
    debug_terminal()