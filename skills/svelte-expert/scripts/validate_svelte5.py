# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
import sys
import json
import re
import argparse
from pathlib import Path

def validate_file(file_path: str) -> dict:
    """Validates a Svelte file for legacy syntax to ensure Svelte 5 compliance."""
    path = Path(file_path)
    if not path.exists():
        return {"status": "error", "message": f"File not found: {file_path}"}
    
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
         return {"status": "error", "message": f"Failed to read file: {e}"}

    errors = []
    
    # Check for legacy export let
    if re.search(r'\bexport\s+let\b', content):
        errors.append("Legacy 'export let' syntax detected. Use '$props()' instead.")
        
    # Check for legacy event modifiers like on:click
    if re.search(r'\s+on:[a-zA-Z]+[=>]', content):
        errors.append("Legacy event modifier 'on:' detected. Use modern event handlers (e.g., 'onclick').")
        
    # Check for legacy reactive statements
    if re.search(r'^\s*\$:\s+', content, re.MULTILINE):
        errors.append("Legacy '$:' reactive statement detected. Use '$derived()' or '$effect()'.")
        
    if errors:
        return {"status": "failed", "errors": errors}
    
    return {"status": "passed", "message": "No legacy Svelte 4 syntax detected. File is structurally compliant with Svelte 5 mandates."}

def main():
    parser = argparse.ArgumentParser(description="Validate Svelte 5 component syntax.")
    parser.add_argument("--file", required=True, help="Path to the .svelte file to validate")
    args = parser.parse_args()
    
    result = validate_file(args.file)
    
    if result.get("status") == "error":
        sys.stderr.write(f"Error: {result['message']}\n")
        print(json.dumps(result, indent=2))
        sys.exit(1)
    elif result["status"] == "failed":
        sys.stderr.write("Validation failed due to legacy syntax.\n")
        print(json.dumps(result, indent=2))
        sys.exit(1)
    else:
        sys.stderr.write("Validation passed.\n")
        print(json.dumps(result, indent=2))
        sys.exit(0)

if __name__ == "__main__":
    main()
