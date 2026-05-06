#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
from pathlib import Path

def run_cmd(cmd, cwd, fail_hard=False):
    """Executes a shell command, returning the result and output."""
    result = subprocess.run(
        cmd, 
        cwd=cwd, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        text=True
    )
    if result.returncode != 0 and fail_hard:
        print(f"[ERROR] Command failed: {' '.join(cmd)}")
        print(f"STDOUT:\n{result.stdout.strip()}")
        print(f"STDERR:\n{result.stderr.strip()}")
        sys.exit(1)
    return result

def main():
    parser = argparse.ArgumentParser(
        description="Collision-resistant Git synchronization for GitHub Wikis."
    )
    parser.add_argument("wiki_dir", type=str, help="Absolute or relative path to the local .wiki.git directory")
    parser.add_argument("message", type=str, help="Commit message")
    args = parser.parse_args()

    wiki_path = Path(args.wiki_dir).resolve()

    if not (wiki_path / '.git').is_dir():
        print(f"[FATAL] Directory '{wiki_path}' is not a valid Git repository.")
        sys.exit(1)

    print(f"[INFO] Initiating sync for: {wiki_path}")

    # 1. Stage all changes (including deletions)
    run_cmd(["git", "add", "-A"], cwd=wiki_path, fail_hard=True)

    # 2. Check for changes
    status_check = run_cmd(["git", "status", "--porcelain"], cwd=wiki_path)
    if not status_check.stdout.strip():
        print("[INFO] Working tree clean. No changes to commit or push.")
        sys.exit(0)

    # 3. Commit
    print(f"[INFO] Staged changes detected. Committing with message: '{args.message}'")
    run_cmd(["git", "commit", "-m", args.message], cwd=wiki_path, fail_hard=True)

    # 4. Push with Collision Detection Loop
    max_retries = 2
    for attempt in range(1, max_retries + 1):
        print(f"[INFO] Attempting to push to remote (Attempt {attempt}/{max_retries})...")
        push_result = run_cmd(["git", "push"], cwd=wiki_path)

        if push_result.returncode == 0:
            print("[SUCCESS] Wiki synchronized successfully.")
            sys.exit(0)
            
        print("[WARN] Push rejected. Remote state likely diverged (e.g., Web UI edits).")
        
        if attempt < max_retries:
            print("[INFO] Attempting automatic rebase to resolve collision...")
            
            # Pull with rebase to layer local commits on top of remote changes
            pull_result = run_cmd(["git", "pull", "--rebase"], cwd=wiki_path)
            
            if pull_result.returncode != 0:
                print("[ERROR] Automatic rebase failed. Manual intervention required (merge conflict).")
                print(f"STDERR:\n{pull_result.stderr.strip()}")
                
                # Abort the rebase to leave the directory in a clean, predictable state for the agent
                run_cmd(["git", "rebase", "--abort"], cwd=wiki_path)
                sys.exit(1)
                
            print("[INFO] Rebase successful. Retrying push...")
        else:
            print("[ERROR] Max push retries exceeded. Synchronization failed.")
            print(f"STDERR:\n{push_result.stderr.strip()}")
            sys.exit(1)

if __name__ == "__main__":
    main()