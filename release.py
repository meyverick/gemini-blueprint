#!/usr/bin/env python3
"""
Automated Release Orchestrator for Gemini Blueprint
Handles version bumping, changelog promotion, manifest syncing, and git tagging.
Requirements: Python 3.8+
"""

import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Configuration
MANIFEST_FILE = Path("gemini-extension.json")
CHANGELOG_FILE = Path("CHANGELOG.md")

# Visual Constants
COLORS = {
    "YELLOW": "\x1b[33m",
    "GREEN": "\x1b[32m",
    "RED": "\x1b[31m",
    "CYAN": "\x1b[36m",
    "NC": "\x1b[0m"
}

def run_cmd(command, check=True):
    """Executes a shell command."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=check,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"{COLORS['RED']}Error executing: {command}{COLORS['NC']}")
        print(e.stderr)
        sys.exit(1)

def get_current_version():
    """Reads version from gemini-extension.json."""
    if not MANIFEST_FILE.exists():
        print(f"{COLORS['RED']}Error: {MANIFEST_FILE} not found.{COLORS['NC']}")
        sys.exit(1)
    
    with open(MANIFEST_FILE, "r") as f:
        data = json.load(f)
        return data.get("version", "0.0.0")

def update_manifest(new_version):
    """Updates the version in gemini-extension.json."""
    with open(MANIFEST_FILE, "r") as f:
        data = json.load(f)
    
    data["version"] = new_version
    
    with open(MANIFEST_FILE, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    print(f"{COLORS['GREEN']}Updated {MANIFEST_FILE} to v{new_version}{COLORS['NC']}")

def get_bump_type(changelog_content):
    """Determines bump type based on unreleased sections."""
    unreleased_match = re.search(r"## \[Unreleased\](.*?)(?=## \[|$)", changelog_content, re.S)
    if not unreleased_match:
        return "patch"
    
    unreleased_text = unreleased_match.group(1).lower()
    
    if "removed" in unreleased_text or "deprecated" in unreleased_text:
        return "major"
    if "added" in unreleased_text:
        return "minor"
    return "patch"

def bump_version(current, bump_type):
    """Calculates the next version string."""
    major, minor, patch = map(int, current.split("."))
    
    if bump_type == "major":
        return f"{major + 1}.0.0"
    if bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"

def promote_changelog(new_version):
    """Promotes [Unreleased] section to a versioned section."""
    if not CHANGELOG_FILE.exists():
        print(f"{COLORS['RED']}Error: {CHANGELOG_FILE} not found.{COLORS['NC']}")
        sys.exit(1)

    with open(CHANGELOG_FILE, "r") as f:
        content = f.read()

    # Check if there are unreleased changes
    unreleased_pattern = r"## \[Unreleased\]\s*\n(.*?)(?=\n## \[|$)"
    match = re.search(unreleased_pattern, content, re.S)
    
    if not match or not match.group(1).strip():
        print(f"{COLORS['YELLOW']}No unreleased changes found in {CHANGELOG_FILE}.{COLORS['NC']}")
        return False

    today = datetime.now().strftime("%Y-%m-%d")
    new_header = f"## [Unreleased]\n\n## [{new_version}] - {today}"
    
    updated_content = content.replace("## [Unreleased]", new_header)
    
    with open(CHANGELOG_FILE, "w") as f:
        f.write(updated_content)
    
    print(f"{COLORS['GREEN']}Promoted unreleased changes to v{new_version} in {CHANGELOG_FILE}{COLORS['NC']}")
    return True

def main():
    print(f"{COLORS['CYAN']}🚀 Starting Automated Release Process...{COLORS['NC']}\n")

    # 1. Check for uncommitted changes
    status = run_cmd("git status --short")
    if status:
        print(f"{COLORS['RED']}Error: Uncommitted changes detected. Please commit or stash them first.{COLORS['NC']}")
        sys.exit(1)

    # 2. Determine versions
    current_version = get_current_version()
    
    with open(CHANGELOG_FILE, "r") as f:
        changelog_content = f.read()
    
    bump_type = get_bump_type(changelog_content)
    new_version = bump_version(current_version, bump_type)

    print(f"Current Version: {current_version}")
    print(f"Bump Type:       {bump_type.upper()}")
    print(f"New Version:     {COLORS['YELLOW']}{new_version}{COLORS['NC']}\n")

    # 3. Apply changes
    if not promote_changelog(new_version):
        print(f"{COLORS['RED']}Release aborted: No content to release.{COLORS['NC']}")
        sys.exit(1)
        
    update_manifest(new_version)

    # 4. Git Operations
    print(f"\n{COLORS['CYAN']}📦 Orchestrating Git sequence...{COLORS['NC']}")
    run_cmd(f'git add {MANIFEST_FILE} {CHANGELOG_FILE}')
    run_cmd(f'git commit -m "chore(release): {new_version}"')
    run_cmd(f'git tag -a v{new_version} -m "Release v{new_version}"')

    # 5. Push
    confirm = input(f"\nPush changes and tag v{new_version} to origin? (y/n): ").lower()
    if confirm == 'y':
        run_cmd("git push origin main")
        run_cmd(f"git push origin v{new_version}")
        print(f"\n{COLORS['GREEN']}✅ Release v{new_version} successfully pushed!{COLORS['NC']}")
    else:
        print(f"\n{COLORS['YELLOW']}Release committed and tagged locally, but not pushed.{COLORS['NC']}")

if __name__ == "__main__":
    main()
