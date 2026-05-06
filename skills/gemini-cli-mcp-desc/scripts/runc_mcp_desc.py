#!/usr/bin/env python3
"""
Executes the Gemini CLI `/mcp desc` command, handles potential connection
timeouts to the MCP server, and ensures valid JSON schema returns.
"""

import argparse
import subprocess
import json
import sys

def run_gemini_mcp_desc(target: str, tool: str = None) -> None:
    # Construct the command enforcing JSON output
    command = ["gemini", "/mcp", "desc", target]
    if tool:
        command.append(tool)
    command.append("--format=json")
    
    try:
        # 10-second timeout to account for local MCP cold-starts
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10.0,
            check=False
        )
    except FileNotFoundError:
        print(json.dumps({"error": "gemini CLI executable not found in PATH."}))
        sys.exit(3)
    except subprocess.TimeoutExpired:
        print(json.dumps({
            "error": "Timeout",
            "message": f"The MCP server '{target}' failed to respond within 10 seconds. It may be offline or initializing."
        }))
        sys.exit(1)

    if result.returncode != 0:
        print(json.dumps({
            "error": "CLI execution or MCP connection failed",
            "stderr": result.stderr.strip()
        }))
        sys.exit(2)

    # Strict Validation Loop
    try:
        parsed_data = json.loads(result.stdout)
        
        # Ensure it maps to expected MCP capability structure
        if "name" not in parsed_data:
            raise ValueError("Incomplete schema returned: Missing 'name' property.")
            
        print(json.dumps(parsed_data, indent=2))
        sys.exit(0)
        
    except (json.JSONDecodeError, ValueError) as e:
        print(json.dumps({
            "error": "Failed to validate CLI output as standard MCP schema.",
            "raw_output": result.stdout[:500] + "... [TRUNCATED]",
            "exception": str(e)
        }))
        sys.exit(2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wrap Gemini CLI /mcp desc")
    parser.add_argument("--target", required=True, help="Name of the MCP server")
    parser.add_argument("--tool", required=False, help="Specific tool on the MCP server to describe")
    args = parser.parse_args()
    
    run_gemini_mcp_desc(args.target, args.tool)