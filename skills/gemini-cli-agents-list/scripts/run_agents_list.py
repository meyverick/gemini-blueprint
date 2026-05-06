#!/usr/bin/env python3
"""
Executes the Gemini CLI `/agents list` command, captures the output, 
and strictly validates it as a JSON payload for the calling agent.
"""

import subprocess
import json
import sys

def run_gemini_cli_agents_list() -> None:
    # Force JSON format to prevent ASCII table generation
    command = ["gemini", "/agents", "list", "--format=json"]
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False
        )
    except FileNotFoundError:
        print(json.dumps({"error": "gemini CLI executable not found in PATH. Verify installation."}))
        sys.exit(2)

    if result.returncode != 0:
        print(json.dumps({
            "error": "CLI execution failed during agent registry lookup.",
            "stderr": result.stderr.strip()
        }))
        sys.exit(1)

    # Strict Validation Loop
    try:
        parsed_data = json.loads(result.stdout)
        
        # Ensure minimum schema shape
        if not isinstance(parsed_data, dict) or "agents" not in parsed_data:
            raise ValueError("Unexpected schema: Missing root 'agents' array.")
            
        print(json.dumps(parsed_data, indent=2))
        sys.exit(0)
        
    except (json.JSONDecodeError, ValueError) as e:
        print(json.dumps({
            "error": "Failed to validate CLI output as structured agent JSON.",
            "raw_output": result.stdout[:500] + "... [TRUNCATED]",
            "exception": str(e)
        }))
        sys.exit(1)

if __name__ == "__main__":
    run_gemini_cli_agents_list()