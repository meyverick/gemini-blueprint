#!/usr/bin/env python3
"""
Cross-Platform Bulk Git Updater (2026)
Handles Windows, macOS, and Linux directory structures.
Requirements: Python 3.8+ installed.
Usage: python update_repos.py
"""

import sys
import subprocess
import re
import io
import os
from pathlib import Path
from typing import List

# Ensure UTF-8 encoding for stdout and stderr to handle emojis on all platforms
if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if isinstance(sys.stderr, io.TextIOWrapper):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Visual Constants
COLORS = {
    "YELLOW": "",
    "GREEN": "",
    "RED": "",
    "CYAN": "",
    "NC": ""
}

def run_cmd(command: List[str], cwd: Path, capture_output: bool = False, ignore_errors: bool = False) -> str:
    """Executes a command and returns its stripped output."""
    try:
        result = subprocess.run(
            command,
            cwd=str(cwd),
            check=True,
            capture_output=capture_output,
            text=True
        )
        return result.stdout.strip() if capture_output else ""
    except subprocess.CalledProcessError:
        if not ignore_errors:
            raise
        return ""

def update_directory(target_dir: Path, description: str) -> None:
    target_dir = target_dir.resolve()
    print(f"{COLORS['CYAN']}🚀 Starting Bulk Repository Sync for {description}...{COLORS['NC']}")
    print(f"{COLORS['CYAN']}Target Directory: {target_dir}{COLORS['NC']}\n")

    if not target_dir.exists() or not target_dir.is_dir():
        print(f"{COLORS['YELLOW']}Notice: Directory {target_dir} does not exist. Skipping sync for {description}.{COLORS['NC']}")
        return

    # Enable long paths globally for Windows compatibility
    run_cmd(["git", "config", "--global", "core.longpaths", "true"], target_dir, capture_output=True, ignore_errors=True)

    # Update existing Subdirectories
    for repo_path in target_dir.iterdir():
        if not repo_path.is_dir():
            continue
            
        git_path = repo_path / '.git'
        
        if git_path.exists():
            # We already updated it if it was in the '.repos' list above, 
            # but this loop handles repos NOT in the list or ensures they are current.
            print(f"{COLORS['YELLOW']}🔄 Checking for updates in [{repo_path.name}]...{COLORS['NC']}")

            try:
                # Check for uncommitted changes (dirty state)
                is_dirty = run_cmd(["git", "status", "--short"], repo_path, capture_output=True)

                if is_dirty:
                    print(f"{COLORS['RED']}  >> Skipped: Uncommitted changes detected.{COLORS['NC']}")
                    continue

                # Determine Default Branch (main or master)
                default_branch = run_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo_path, capture_output=True)

                # Perform the Fast-Forward Pull
                run_cmd(["git", "pull", "--ff-only", "origin", default_branch, "--prune"], repo_path, capture_output=True)

                print(f"{COLORS['GREEN']}  >> Successfully updated.{COLORS['NC']}")
            except subprocess.CalledProcessError:
                print(f"{COLORS['RED']}  >> Failed: Diverged history or network error.{COLORS['NC']}", file=sys.stderr)
                
            print('------------------------------------')

    print(f"\n{COLORS['GREEN']}✅ Process completed for {description}.{COLORS['NC']}\n")

def update_repositories() -> None:
    # Resolve the current working directory (the Workspace directory)
    workspace_root = Path.cwd().resolve()
    workspace_dir = (workspace_root / 'references' / 'repositories').resolve()
    
    print(f"{COLORS['CYAN']}🔍 Path Discovery:{COLORS['NC']}")
    print(f"   Workspace Root: {workspace_root}\n")

    # Sync Workspace repositories
    update_directory(workspace_dir, "Workspace")

if __name__ == "__main__":
    update_repositories()