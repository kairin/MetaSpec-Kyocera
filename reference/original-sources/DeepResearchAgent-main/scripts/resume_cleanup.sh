#!/bin/bash
# Terminal cleanup script for Claude Code session resume

echo "🧹 Cleaning up terminal state from previous session..."

# Disable all mouse tracking modes
printf '\033[?1000l'    # Disable X11 mouse reporting
printf '\033[?1002l'    # Disable cell motion mouse tracking
printf '\033[?1003l'    # Disable all motion mouse tracking
printf '\033[?1006l'    # Disable SGR mouse mode
printf '\033[?1015l'    # Disable urxvt mouse mode
printf '\033[?25h'      # Show cursor
printf '\033[?1049l'    # Exit alternate screen
printf '\033[?1004l'    # Disable focus reporting
printf '\033[?2004l'    # Disable bracketed paste

# Reset terminal to sane state
stty sane 2>/dev/null || true
reset 2>/dev/null || true

echo "✅ Terminal cleanup complete"
echo "Mouse tracking disabled, terminal state reset"