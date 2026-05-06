#!/usr/bin/env python3
"""
Repository Constraint Auditor
Deterministically verifies branch counts, disk size, and file density limits.
"""

import os
import sys
import subprocess

MAX_BRANCHES = 5000
MAX_STORAGE_GB = 10
MAX_FILES_PER_DIR = 3000
MAX_DEPTH = 50

def get_dir_size(path='.'):
    """Calculate total size of the directory tree in bytes."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

def get_branch_count():
    """Retrieve total number of branches (local + remote)."""
    try:
        result = subprocess.run(['git', 'branch', '-a'], capture_output=True, text=True, check=True)
        return len([line for line in result.stdout.split('\n') if line.strip()])
    except subprocess.CalledProcessError:
        return 0 # Not a git repository, skip branch check

def audit_directory_density(path='.'):
    """Check for maximum depth and file density per directory."""
    violations = []
    base_depth = path.count(os.sep)
    
    for dirpath, dirnames, filenames in os.walk(path):
        # Ignore hidden folders like .git
        if '.git' in dirpath:
            continue
            
        current_depth = dirpath.count(os.sep) - base_depth
        if current_depth > MAX_DEPTH:
            violations.append(f"Depth violation: {dirpath} (Depth: {current_depth})")
            
        if len(filenames) > MAX_FILES_PER_DIR:
            violations.append(f"Density violation: {dirpath} contains {len(filenames)} files.")
            
    return violations

def main():
    print("Executing Repository Constraint Audit...")
    
    # 1. Branch Limit Audit
    branch_count = get_branch_count()
    if branch_count > MAX_BRANCHES:
        print(f"[!] VIOLATION: Branch count ({branch_count}) exceeds maximum limit ({MAX_BRANCHES}).")
        sys.exit(1)
        
    # 2. Storage Limit Audit
    size_bytes = get_dir_size()
    size_gb = size_bytes / (1024 ** 3)
    if size_gb > MAX_STORAGE_GB:
        print(f"[!] VIOLATION: On-disk size ({size_gb:.2f} GB) exceeds maximum limit ({MAX_STORAGE_GB} GB).")
        sys.exit(1)
        
    # 3. Density & Depth Audit
    density_violations = audit_directory_density()
    if density_violations:
        print("[!] VIOLATION: Directory structure limits exceeded:")
        for v in density_violations[:5]: # Print first 5 violations
            print(f"  - {v}")
        if len(density_violations) > 5:
            print(f"  ...and {len(density_violations) - 5} more.")
        sys.exit(1)

    print("Audit Passed: Repository is within operational bounds.")
    sys.exit(0)

if __name__ == "__main__":
    main()