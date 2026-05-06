#!/usr/bin/env python3
"""
Changelog History Parser
Extracts git history since the last SemVer tag and categorizes commits for the LLM.
"""

import subprocess
import sys
import json

def get_latest_tag():
    """Finds the most recent git tag."""
    try:
        result = subprocess.run(
            ['git', 'describe', '--tags', '--abbrev=0'],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None  # No tags exist

def get_git_history(since_tag=None):
    """Retrieves commit history."""
    range_str = f"{since_tag}..HEAD" if since_tag else "HEAD"
    cmd = ['git', 'log', range_str, '--pretty=format:%h|%s|%ad', '--date=short']
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        lines = [line for line in result.stdout.split('\n') if line.strip()]
        
        history = []
        for line in lines:
            parts = line.split('|', 2)
            if len(parts) == 3:
                history.append({"hash": parts[0], "message": parts[1], "date": parts[2]})
        return history
    except subprocess.CalledProcessError as e:
        print(json.dumps({"error": f"Git command failed: {str(e)}"}))
        sys.exit(1)

def categorize_commit(message):
    """Maps conventional commit messages to Keep a Changelog categories."""
    msg = message.lower()
    if msg.startswith('feat') or 'added' in msg:
        return 'Added'
    if msg.startswith('fix') or 'fixed' in msg:
        return 'Fixed'
    if 'security' in msg or 'vuln' in msg or 'cve' in msg:
        return 'Security'
    if 'deprecate' in msg:
        return 'Deprecated'
    if 'remove' in msg or 'drop' in msg:
        return 'Removed'
    return 'Changed'  # Default for refactor, perf, chore, etc.

def main():
    latest_tag = get_latest_tag()
    history = get_git_history(latest_tag)
    
    report = []
    for entry in history:
        # Skip merge commits or trivial changes
        if entry['message'].startswith('Merge') or entry['message'].startswith('chore'):
            continue
            
        entry['category'] = categorize_commit(entry['message'])
        report.append(entry)
    
    # Output structured payload for the agent
    payload = {
        "metadata": {
            "since_tag": latest_tag if latest_tag else "repository_root",
            "commit_count": len(report)
        },
        "commits": report
    }
    
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()