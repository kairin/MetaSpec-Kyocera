#!/usr/bin/env python3
"""Minimal TUI test to debug terminal rendering issues."""

import sys
from textual.app import App, ComposeResult
from textual.widgets import Label, Button
from textual.containers import Vertical

class MinimalTUI(App):
    """Minimal TUI for testing."""

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("🧪 Minimal TUI Test", id="title")
            yield Label("If you see this cleanly, Textual is working!")
            yield Button("Test Button", id="test_button")
            yield Label("Press 'q' to quit")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "test_button":
            self.query_one("#title", Label).update("✅ Button clicked!")

    def on_key(self, event) -> None:
        if event.key == "q":
            self.exit()

if __name__ == "__main__":
    # Check terminal compatibility
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        print("❌ Requires an interactive terminal")
        sys.exit(1)

    print("Testing minimal TUI...")
    print("If you see escape sequences, there's a terminal compatibility issue")
    print("Press 'q' to quit when the TUI starts")

    app = MinimalTUI()
    app.run()