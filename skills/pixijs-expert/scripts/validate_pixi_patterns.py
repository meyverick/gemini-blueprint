# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

import argparse
import re
import sys
import json
from pathlib import Path

def validate_pixi_file(filepath: str) -> dict:
    path = Path(filepath)
    if not path.exists():
        return {"status": "error", "message": f"File not found: {filepath}"}

    content = path.read_text(encoding="utf-8")
    issues = []

    # Check 1: Law of Demeter violation (deep child/parent access)
    # e.g., getChildAt(0).getChildByName or .parent.parent
    if re.search(r'\.getChild(?:At|ByName)\([^)]+\)\.getChild', content) or re.search(r'\.parent\.parent', content):
        issues.append({
            "rule": "Law of Demeter",
            "severity": "High",
            "message": "Deep scene graph traversal detected. Components must only interact with immediate children."
        })

    # Check 2: Reactive Proxy Leak
    # Looking for signs of putting PIXI objects in reactive wrappers (very heuristic)
    if re.search(r'\$state\(\s*new\s+(?:PIXI\.)?(?:Sprite|Container|Graphics|Texture)', content) or re.search(r'ref\(\s*new\s+(?:PIXI\.)?(?:Sprite|Container)', content):
        issues.append({
            "rule": "State Management SoC",
            "severity": "Critical",
            "message": "PixiJS display objects detected inside reactive state primitives. This causes proxy bloat and memory leaks."
        })

    # Check 3: Ticker Memory Leaks (Adding anonymous functions to Ticker)
    if re.search(r'Ticker\.shared\.add\(\s*(?:\([^)]*\)\s*=>|function)', content):
        issues.append({
            "rule": "Memory Management",
            "severity": "Medium",
            "message": "Anonymous function added to Ticker. This cannot be easily removed and often causes memory leaks. Bind explicit methods instead."
        })

    # Check 4: Missing destroy logic for Ticker/Events in classes extending Container
    has_class_extending_container = bool(re.search(r'class\s+\w+\s+extends\s+(?:PIXI\.)?Container', content))
    if has_class_extending_container:
        if 'Ticker.shared.add(' in content and 'Ticker.shared.remove(' not in content:
            issues.append({
                "rule": "Memory Management",
                "severity": "High",
                "message": "Class adds Ticker listener but never calls Ticker.shared.remove(). Implement destruction logic."
            })
        if not re.search(r'destroy\s*\(', content):
            issues.append({
                "rule": "Memory Management",
                "severity": "Low",
                "message": "Custom Container subclass lacks a destroy() method override. Ensure resources are explicitly freed."
            })

    result = {
        "status": "success" if not issues else "failed",
        "file": str(path),
        "issues": issues
    }
    return result

def main():
    parser = argparse.ArgumentParser(description="Validate PixiJS code for architecture anti-patterns.")
    parser.add_argument("--file", required=True, help="Path to the TS/JS file to validate")
    args = parser.parse_args()

    result = validate_pixi_file(args.file)
    
    if result["status"] == "error":
        print(json.dumps(result, indent=2), file=sys.stderr)
        sys.exit(1)
        
    print(json.dumps(result, indent=2))
    
    if result["status"] == "failed":
        sys.exit(1)

if __name__ == "__main__":
    main()
