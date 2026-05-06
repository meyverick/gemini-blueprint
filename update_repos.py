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
from pathlib import Path
from typing import List

# Visual Constants
COLORS = {
    "YELLOW": "\x1b[33m",
    "GREEN": "\x1b[32m",
    "RED": "\x1b[31m",
    "CYAN": "\x1b[36m",
    "NC": "\x1b[0m"
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
    print(f"{COLORS['CYAN']}🚀 Starting Bulk Repository Sync for {description}...{COLORS['NC']}")
    print(f"{COLORS['CYAN']}Target Directory: {target_dir}{COLORS['NC']}\n")

    if not target_dir.exists() or not target_dir.is_dir():
        print(f"{COLORS['YELLOW']}Notice: Directory {target_dir} does not exist. Skipping sync for {description}.{COLORS['NC']}")
        return

    # Clone missing repositories from 'repositories' file
    repos_file_path = target_dir / 'repositories'
    if repos_file_path.exists():
        print(f"{COLORS['CYAN']}📄 Checking missing repositories from 'repositories' file...{COLORS['NC']}\n")
        
        with open(repos_file_path, "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
        
        for url in urls:
            match = re.search(r'/([^/]+?)(?:\.git)?$', url)
            if match:
                repo_name = match.group(1)
                repo_path = target_dir / repo_name

                if not repo_path.exists():
                    print(f"{COLORS['YELLOW']}📦 Cloning missing repository: [{repo_name}]...{COLORS['NC']}")
                    try:
                        subprocess.run(["git", "clone", url], cwd=str(target_dir), check=True)
                        print(f"{COLORS['GREEN']}  >> Successfully cloned.{COLORS['NC']}")
                    except subprocess.CalledProcessError:
                        print(f"{COLORS['RED']}  >> Failed to clone {url}.{COLORS['NC']}", file=sys.stderr)
                    print('------------------------------------')

    # Enable long paths globally for Windows compatibility
    run_cmd(["git", "config", "--global", "core.longpaths", "true"], target_dir, capture_output=True, ignore_errors=True)

    # Read Subdirectories
    for repo_path in target_dir.iterdir():
        if not repo_path.is_dir():
            continue
            
        git_path = repo_path / '.git'
        
        if git_path.exists():
            print(f"{COLORS['YELLOW']}📦 Updating [{repo_path.name}]...{COLORS['NC']}")

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

                print(f"{COLORS['GREEN']}  >> Successfully synchronized.{COLORS['NC']}")
            except subprocess.CalledProcessError:
                print(f"{COLORS['RED']}  >> Failed: Diverged history or network error.{COLORS['NC']}", file=sys.stderr)
                
            print('------------------------------------')

    print(f"\n{COLORS['GREEN']}✅ Process completed for {description}.{COLORS['NC']}\n")

def update_repositories() -> None:
    workspace_dir = Path.cwd() / 'references' / 'repositories'
    extension_dir = Path(__file__).resolve().parent / 'references' / 'repositories'
    
    update_directory(extension_dir, "Extension")
    
    if workspace_dir != extension_dir:
        update_directory(workspace_dir, "Workspace")

if __name__ == "__main__":
    update_repositories()