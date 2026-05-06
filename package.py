#!/usr/bin/env python3
"""
Packaging Script for Gemini Blueprint
Creates clean distribution archives for GitHub Releases.
"""

import shutil
import os
from pathlib import Path

# Configuration
EXT_NAME = "gemini-blueprint"
DIST_DIR = Path("dist")
ARCHIVE_DIR = Path("release")

# Files and directories to include in the extension distribution
INCLUDE_LIST = [
    "agents",
    "commands",
    "hooks",
    "policies",
    "references",
    "skills",
    "wiki",
    "gemini-extension.json",
    "GEMINI.md",
    "README.md",
    "CHANGELOG.md",
    "LICENSE.md",
    "update_repos.py",
]

def clean():
    """Removes old dist and release directories."""
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    if ARCHIVE_DIR.exists():
        shutil.rmtree(ARCHIVE_DIR)
    DIST_DIR.mkdir()
    ARCHIVE_DIR.mkdir()

def package():
    """Copies included files to the dist directory and creates archives."""
    print(f"📦 Packaging {EXT_NAME}...")
    
    for item in INCLUDE_LIST:
        src = Path(item)
        if not src.exists():
            print(f"⚠️  Warning: {item} not found, skipping.")
            continue
            
        dest = DIST_DIR / item
        if src.is_dir():
            shutil.copytree(src, dest)
        else:
            shutil.copy(src, dest)
    
    # Create archives for different platforms (even if content is identical)
    platforms = [
        ("win32", "zip"),
        ("linux", "gztar"),
        ("darwin", "gztar")
    ]
    
    for platform, format in platforms:
        ext = "zip" if format == "zip" else "tar.gz"
        archive_name = ARCHIVE_DIR / f"{platform}.{EXT_NAME}"
        print(f"  >> Creating {archive_name}.{ext}...")
        shutil.make_archive(str(archive_name), format, DIST_DIR)

    print("\n✅ Packaging complete. Assets are in the 'release/' directory.")

if __name__ == "__main__":
    clean()
    package()
