#!/usr/bin/env python3
"""Emergency terminal cleanup - runs automatically on import to prevent mouse flood."""

import sys
import os
import signal
import time

def emergency_cleanup():
    """Emergency cleanup that runs immediately when imported."""
    try:
        # Disable all mouse tracking immediately
        cleanup_sequences = [
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

        for seq in cleanup_sequences:
            sys.stdout.write(seq)
            sys.stdout.flush()

        # Force terminal reset
        os.system('stty sane 2>/dev/null || true')

    except Exception:
        pass  # Fail silently - this is emergency cleanup

def setup_emergency_handlers():
    """Set up signal handlers for emergency cleanup."""
    def emergency_exit(signum, frame):
        emergency_cleanup()
        sys.exit(0)

    # Handle common interrupt signals
    signal.signal(signal.SIGINT, emergency_exit)   # Ctrl+C
    signal.signal(signal.SIGTERM, emergency_exit)  # Termination

    try:
        signal.signal(signal.SIGQUIT, emergency_exit)  # Ctrl+\
    except AttributeError:
        pass  # Not available on all systems

# Run cleanup immediately when this module is imported
emergency_cleanup()
setup_emergency_handlers()

if __name__ == "__main__":
    print("🚨 Emergency terminal cleanup executed")
    print("Mouse tracking should be disabled now")