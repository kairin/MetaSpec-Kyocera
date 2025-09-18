#!/usr/bin/env python3
"""Simple test to check if Textual works in this environment."""

import asyncio
import sys
import os

# Set terminal type
os.environ['TERM'] = 'xterm-256color'

from textual.app import App
from textual.widgets import Label

class TestApp(App):
    def compose(self):
        yield Label("Textual Test - If you see this, Textual is working!")

async def main():
    app = TestApp()
    try:
        await app.run_async()
        print("✅ Textual test completed successfully!")
        return True
    except Exception as e:
        print(f"❌ Textual test failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)