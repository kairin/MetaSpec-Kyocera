#!/bin/bash
# Wrapper script to run DeepResearchAgent TUI with proper terminal setup

# Save current terminal settings
stty_saved=$(stty -g)

# Function to restore terminal on exit
cleanup() {
    # Restore terminal settings
    stty "$stty_saved" 2>/dev/null || true
    # Reset terminal
    tput reset 2>/dev/null || true
    printf '\e[?1000l\e[?1002l\e[?1003l\e[?1005l\e[?1006l\e[?1015l' 2>/dev/null || true
}

# Set trap to cleanup on exit
trap cleanup EXIT INT TERM

# Reset terminal to known state
tput reset 2>/dev/null || true
stty sane 2>/dev/null || true

# Disable mouse tracking
printf '\e[?1000l' 2>/dev/null || true  # Disable mouse tracking
printf '\e[?1002l' 2>/dev/null || true  # Disable mouse motion tracking
printf '\e[?1003l' 2>/dev/null || true  # Disable all mouse tracking
printf '\e[?1005l' 2>/dev/null || true  # Disable mouse wheel tracking
printf '\e[?1006l' 2>/dev/null || true  # Disable SGR mouse mode
printf '\e[?1015l' 2>/dev/null || true  # Disable URXVT mouse mode

# Set terminal type
export TERM=xterm-256color

# Run the TUI
cd /home/kkk/Apps/DeepResearchAgent
exec uv run python main.py --tui