#!/usr/bin/env python3
"""Terminal cleanup utility to reset mouse tracking and other terminal modes."""

import sys
import os

def reset_terminal():
    """Reset terminal to clean state and disable mouse tracking."""

    # ANSI escape sequences to reset terminal state
    reset_sequences = [
        "\033[?1000l",    # Disable X11 mouse reporting
        "\033[?1002l",    # Disable cell motion mouse tracking
        "\033[?1003l",    # Disable all motion mouse tracking
        "\033[?1006l",    # Disable SGR mouse mode
        "\033[?1015l",    # Disable urxvt mouse mode
        "\033[?25h",      # Show cursor
        "\033[?1049l",    # Exit alternate screen
        "\033[?1004l",    # Disable focus reporting
        "\033[?2004l",    # Disable bracketed paste
        "\033c",          # Full reset
        "\033[0m",        # Reset colors/formatting
    ]

    # Send reset sequences
    for seq in reset_sequences:
        sys.stdout.write(seq)
        sys.stdout.flush()

    # Use system commands for additional cleanup
    try:
        os.system('stty sane')
        os.system('reset')
    except:
        pass

    print("✅ Terminal reset complete - mouse tracking disabled")

def cleanup_on_resume():
    """Cleanup function specifically for session resume."""
    print("🧹 Cleaning up terminal state from previous session...")
    reset_terminal()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--resume":
        cleanup_on_resume()
    else:
        reset_terminal()