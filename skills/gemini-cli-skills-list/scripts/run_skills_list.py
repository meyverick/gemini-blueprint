#!/usr/bin/env python3
"""
Executes the Gemini CLI `/skills list` command, captures the output, 
and ensures it returns a valid JSON schema representing the skill environment.
"""

import subprocess
import json
import sys

def run_gemini_cli_skills_list() -> None:
    # Construct the command enforcing JSON output to avoid ASCII table parsing
    command = ["gemini", "/skills", "list", "--format=json"]
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False
        )
    except FileNotFoundError:
        print(json.dumps({"error": "gemini CLI executable not found in PATH."}))
        sys.exit(2)

    if result.returncode != 0:
        print(json.dumps({
            "error": "CLI execution failed",
            "stderr": result.stderr.strip()
        }))
        sys.exit(1)

    # Strict Validation Loop
    try:
        parsed_data = json.loads(result.stdout)
        
        # Ensure minimum schema requirements for the agent to understand the state
        if not isinstance(parsed_data, list) and "skills" not in parsed_data:
            raise ValueError("Unexpected schema structure returned by CLI.")
            
        print(json.dumps(parsed_data, indent=2))
        sys.exit(0)
        
    except (json.JSONDecodeError, ValueError) as e:
        print(json.dumps({
            "error": "Failed to validate CLI output as a structured skills list.",
            "raw_output": result.stdout[:500] + "... [TRUNCATED]",
            "exception": str(e)
        }))
        sys.exit(1)

if __name__ == "__main__":
    run_gemini_cli_skills_list()