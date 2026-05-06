#!/usr/bin/env python3
"""
Executes the Gemini CLI `/tools desc` command, captures the output, 
and ensures it returns a valid JSON schema for the agent.
"""

import argparse
import subprocess
import json
import sys

def run_gemini_cli_desc(tool_name: str) -> None:
    # Construct the command enforcing JSON output to avoid truncation and parsing errors
    command = ["gemini", "/tools", "desc", tool_name, "--format=json"]
    
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
        # Ensure minimum schema requirements for the agent
        if "name" not in parsed_data or "parameters" not in parsed_data:
            raise ValueError("Incomplete schema returned by CLI.")
            
        print(json.dumps(parsed_data, indent=2))
        sys.exit(0)
        
    except (json.JSONDecodeError, ValueError) as e:
        print(json.dumps({
            "error": "Failed to validate CLI output as standard tool schema.",
            "raw_output": result.stdout[:500] + "... [TRUNCATED]",
            "exception": str(e)
        }))
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wrap Gemini CLI /tools desc")
    parser.add_argument("--tool", required=True, help="Name of the tool to describe")
    args = parser.parse_args()
    
    run_gemini_cli_desc(args.tool)