#!/usr/bin/env python3
"""
Git Branch Manager - Implements timestamp-based branch naming strategy
Format: YYYY-MM-DD-HH-MM-SS-description
"""

import subprocess
import sys
from datetime import datetime
import re


def sanitize_description(text):
    """Convert text to kebab-case for branch name"""
    # Take first 50 chars, lowercase, replace spaces/special chars with hyphens
    text = text[:50].lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text


def generate_branch_name(commit_message):
    """Generate timestamp-based branch name from commit message"""
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d-%H-%M-%S')
    description = sanitize_description(commit_message)
    return f"{timestamp}-{description}"


def run_git_command(command):
    """Execute git command and return output"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return None


def create_and_push_branch(commit_message):
    """Create timestamped branch and push to remote"""
    # Generate branch name
    branch_name = generate_branch_name(commit_message)
    
    print(f"Creating branch: {branch_name}")
    
    # Get current branch
    current_branch = run_git_command("git branch --show-current")
    if not current_branch:
        print("Error: Could not determine current branch")
        return False
    
    # Stage all changes
    print("Staging all changes...")
    run_git_command("git add -A")
    
    # Commit changes
    print(f"Committing with message: {commit_message}")
    commit_cmd = f'git commit -m "{commit_message}"'
    if not run_git_command(commit_cmd):
        print("Warning: No changes to commit or commit failed")
    
    # Create new branch from current HEAD
    print(f"Creating branch {branch_name}...")
    if not run_git_command(f"git checkout -b {branch_name}"):
        print(f"Error: Could not create branch {branch_name}")
        return False
    
    # Push new branch to remote
    print(f"Pushing {branch_name} to remote...")
    if not run_git_command(f"git push -u origin {branch_name}"):
        print(f"Error: Could not push branch {branch_name}")
        return False
    
    # Switch back to main
    print("Switching back to main branch...")
    run_git_command("git checkout main")
    
    # Merge the changes to main (fast-forward if possible)
    print("Merging changes to main...")
    run_git_command(f"git merge {branch_name}")
    
    # Push main
    print("Pushing main to remote...")
    run_git_command("git push origin main")
    
    print(f"\nSuccess! Branch {branch_name} created and pushed.")
    print(f"Main branch updated with changes.")
    print(f"History preserved in branch: {branch_name}")
    
    return True


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python git_branch_manager.py 'commit message'")
        sys.exit(1)
    
    commit_message = ' '.join(sys.argv[1:])
    
    if create_and_push_branch(commit_message):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()