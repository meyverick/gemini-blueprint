#!/usr/bin/env python3
"""
scripts/validate_env.py
Validates the presence of required Svelte MCP binaries or local environment configs.
"""
import sys
import shutil

def check_dependencies():
    required_commands = ["node", "npm"]
    missing = [cmd for cmd in required_commands if shutil.which(cmd) is None]
    
    if missing:
        print(f"Error: Missing required execution dependencies: {', '.join(missing)}")
        sys.exit(1)
    
    print("Environment validation passed. Svelte execution context ready.")
    sys.exit(0)

if __name__ == "__main__":
    check_dependencies()