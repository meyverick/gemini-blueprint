# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

import json
import sys
import os
import argparse

def validate_setup(target_dir: str):
    """Validates the Tauri project structure and basic configuration."""
    tauri_conf_path = os.path.join(target_dir, "src-tauri", "tauri.conf.json")
    
    if not os.path.exists(tauri_conf_path):
        sys.stderr.write(f"Diagnostic: tauri.conf.json not found in {tauri_conf_path}\n")
        print(json.dumps({"valid": False, "error": "Missing tauri.conf.json"}))
        sys.exit(1)

    try:
        with open(tauri_conf_path, 'r', encoding='utf-8') as f:
            conf = json.load(f)
    except Exception as e:
        sys.stderr.write(f"Diagnostic: Failed to parse tauri.conf.json: {str(e)}\n")
        print(json.dumps({"valid": False, "error": "Invalid JSON format"}))
        sys.exit(1)

    issues = []
    
    if not conf.get("identifier"):
        issues.append("Missing application identifier.")

    if issues:
        sys.stderr.write("Diagnostic: Tauri configuration validation failed.\n")
        print(json.dumps({"valid": False, "issues": issues}))
        sys.exit(1)
        
    sys.stderr.write("Diagnostic: Tauri configuration validation passed.\n")
    print(json.dumps({"valid": True, "message": "Tauri configuration adheres to baseline expectations."}))
    sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate Tauri v2 project constraints.")
    parser.add_argument("--path", default=".", help="Root path of the project")
    args = parser.parse_args()
    validate_setup(args.path)
