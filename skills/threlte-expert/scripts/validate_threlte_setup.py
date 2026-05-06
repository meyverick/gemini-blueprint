# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
import sys
import json
from pathlib import Path

def validate_environment():
    try:
        package_path = Path.cwd() / "package.json"
        if not package_path.exists():
            print(json.dumps({"status": "error", "message": "package.json not found in current working directory."}))
            sys.exit(1)
            
        with open(package_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        dependencies = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
        
        svelte_ver = dependencies.get("svelte", "")
        threlte_ver = dependencies.get("@threlte/core", "")
        
        issues = []
        if not svelte_ver.startswith("^5") and not svelte_ver.startswith("5") and "next" not in svelte_ver:
            issues.append(f"Requires Svelte 5. Found: {svelte_ver}")
            
        if not threlte_ver.startswith("^8") and not threlte_ver.startswith("8") and "next" not in threlte_ver:
            issues.append(f"Requires Threlte v8+. Found: {threlte_ver}")
            
        if issues:
            print(json.dumps({"status": "failed", "issues": issues}))
            sys.exit(1)
            
        print(json.dumps({"status": "success", "message": "Environment validated for Svelte 5 and Threlte v8+."}))
        sys.exit(0)
        
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    validate_environment()