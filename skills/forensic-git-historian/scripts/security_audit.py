#!/usr/bin/env python3
"""
Watchtower Security Audit Script
Validates the git index against strict security exclusions prior to commit generation.
"""

import subprocess
import sys
import os

SENSITIVE_EXTENSIONS = {'.pem', '.key', '.env', '.log', '.sqlite3'}
RESTRICTED_DIRECTORIES = {'node_modules', 'dist', 'build', '.vscode', '.idea', '__pycache__'}

def get_staged_files():
    """Retrieves a list of currently staged files."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--name-only', '--cached'],
            capture_output=True, text=True, check=True
        )
        return [line.strip() for line in result.stdout.split('\n') if line.strip()]
    except subprocess.CalledProcessError:
        print("ERROR: Failed to read git index. Is this a git repository?")
        sys.exit(1)

def audit_staged_files(staged_files):
    """Audits staged files against security constraints."""
    violations = []

    for filepath in staged_files:
        filename = os.path.basename(filepath)
        _, ext = os.path.splitext(filename)
        path_parts = set(filepath.split(os.sep))

        # Check for sensitive extensions
        if ext.lower() in SENSITIVE_EXTENSIONS or filename.lower() in SENSITIVE_EXTENSIONS:
            violations.append(f"Sensitive file extension or name detected: {filepath}")
        
        # Check for restricted directories
        intersecting_dirs = path_parts.intersection(RESTRICTED_DIRECTORIES)
        if intersecting_dirs:
            violations.append(f"Restricted directory staged ({', '.join(intersecting_dirs)}): {filepath}")

    return violations

def main():
    print("Initiating Watchtower Security Audit...")
    staged_files = get_staged_files()
    
    if not staged_files:
        print("WARNING: No files currently staged for commit.")
        sys.exit(0)

    violations = audit_staged_files(staged_files)

    if violations:
        print("\n[!] SECURITY AUDIT FAILED. The following violations were detected in the staging area:\n")
        for violation in violations:
            print(f"  - {violation}")
        print("\nACTION REQUIRED: Unstage these files (e.g., `git reset HEAD <file>`) and update .gitignore before proceeding.")
        sys.exit(1)

    print("Watchtower Audit Passed: No sensitive artifacts detected in staging area.")
    sys.exit(0)

if __name__ == "__main__":
    main()