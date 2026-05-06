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
    "skills",
    "wiki",
    "gemini-extension.json",
    "GEMINI.md",
    "README.md",
    "CHANGELOG.md",
    "LICENSE.md",
    "update_repos.py",
]

def rmtree_error_handler(func, path, exc_info):
    """
    Error handler for shutil.rmtree.
    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.
    """
    import stat
    
    # Handle the path being a directory or a file
    try:
        if os.path.isdir(path):
            os.chmod(path, stat.S_IWRITE)
        else:
            os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception as e:
        # If chmod + retry fails, it's likely a file lock. 
        # We can't do much about locks in a script, but we can try to be less disruptive.
        print(f"  >> Notice: Could not remove {path}: {e}")

def clean():
    """Removes old dist and release directories."""
    # Try a simple rmtree first, then fall back to error handler
    for target in [DIST_DIR, ARCHIVE_DIR]:
        if target.exists():
            try:
                shutil.rmtree(target, onerror=rmtree_error_handler)
            except Exception as e:
                print(f"⚠️  Warning: Could not fully clean {target}: {e}")
    
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

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

    # Clean up transient build directory
    print(f"\n🧹 Cleaning up transient build directory...")
    shutil.rmtree(DIST_DIR, onerror=rmtree_error_handler)

    print(f"\n✅ Packaging complete. Assets are in the '{ARCHIVE_DIR}/' directory.")


if __name__ == "__main__":
    clean()
    package()
