#!/usr/bin/env python3
"""
Script to print the current system date in YYYY-MM-DD format.
"""
from datetime import datetime

def main():
    print(datetime.now().strftime('%Y-%m-%d'))

if __name__ == "__main__":
    main()
