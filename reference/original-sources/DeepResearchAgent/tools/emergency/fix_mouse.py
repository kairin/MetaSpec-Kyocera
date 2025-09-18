#!/usr/bin/env python3
"""Quick fix for mouse escape sequences."""

import sys

def fix_mouse_tracking():
    """Disable mouse tracking that causes escape sequences."""

    print("🔧 Disabling mouse tracking...")

    # Disable all mouse tracking modes
    sequences = [
        "\033[?1000l",    # Disable X11 mouse reporting
        "\033[?1002l",    # Disable cell motion mouse tracking
        "\033[?1003l",    # Disable all motion mouse tracking
        "\033[?1006l",    # Disable SGR mouse mode
        "\033[?1015l",    # Disable urxvt mouse mode
        "\033[?25h",      # Show cursor
        "\033[?1049l",    # Exit alternate screen
        "\033[?1004l",    # Disable focus reporting
        "\033[?2004l",    # Disable bracketed paste
    ]

    for seq in sequences:
        sys.stdout.write(seq)
        sys.stdout.flush()

    print("✅ Mouse tracking disabled")
    print("Escape sequences should stop appearing now")

if __name__ == "__main__":
    fix_mouse_tracking()