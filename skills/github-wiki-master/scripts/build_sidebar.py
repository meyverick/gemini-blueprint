#!/usr/bin/env python3
import os
import sys
import argparse
from pathlib import Path

def build_tree(base_path: Path) -> dict:
    """
    Recursively builds a nested dictionary representing the markdown directory structure.
    Ignores hidden directories (.git) and system/partial files prefixed with '_'.
    """
    tree = {}
    
    # Sort for deterministic output
    entries = sorted(os.listdir(base_path))
    
    for entry in entries:
        full_path = base_path / entry
        
        # Skip Git internals, image directories, and partials (like _Sidebar.md, _Footer.md)
        if entry.startswith('.') or entry.startswith('_') or entry.lower() == 'images':
            continue
            
        if full_path.is_dir():
            sub_tree = build_tree(full_path)
            # Only add directories if they contain valid markdown files
            if sub_tree:
                tree[entry] = sub_tree
        elif full_path.is_file() and entry.endswith('.md'):
            # Store the stem (filename without .md) for Wiki linking
            tree[entry] = full_path.stem

    return tree

def generate_markdown_list(tree: dict, indent_level: int = 0) -> str:
    """
    Converts the nested tree dictionary into a GFM-compliant nested unordered list.
    """
    md_lines = []
    indent = "  " * indent_level
    
    for key, value in tree.items():
        if isinstance(value, dict):
            # It's a directory
            dir_name = key.replace('-', ' ').title()
            md_lines.append(f"{indent}* **{dir_name}**")
            md_lines.append(generate_markdown_list(value, indent_level + 1))
        else:
            # It's a file. Format as a GitHub Wiki Link: [[Page-Name]] or [[Display Text|Page-Name]]
            display_name = value.replace('-', ' ')
            # If the filename already matches the display name exactly, use simple syntax
            if display_name == value:
                md_lines.append(f"{indent}* [[{value}]]")
            else:
                md_lines.append(f"{indent}* [[{display_name}|{value}]]")
                
    return "\n".join(md_lines)

def main():
    parser = argparse.ArgumentParser(
        description="Auto-generates _Sidebar.md based on the current markdown directory structure."
    )
    parser.add_argument("wiki_dir", type=str, help="Absolute or relative path to the local .wiki.git directory")
    args = parser.parse_args()

    wiki_path = Path(args.wiki_dir).resolve()
    
    if not wiki_path.is_dir():
        print(f"[FATAL] Directory '{wiki_path}' does not exist.")
        sys.exit(1)

    print(f"[INFO] Mapping directory structure at: {wiki_path}")
    
    # 1. Map the directory
    nav_tree = build_tree(wiki_path)
    
    # 2. Inject Home page at the top if it exists
    sidebar_content = []
    sidebar_content.append("## Navigation\n")
    
    home_path = wiki_path / "Home.md"
    if home_path.exists():
        sidebar_content.append("* [[Home]]")
        # Remove Home from the tree so it doesn't duplicate in the list
        if "Home.md" in nav_tree:
            del nav_tree["Home.md"]
            
    # 3. Generate the rest of the list
    sidebar_content.append(generate_markdown_list(nav_tree))
    
    # 4. Write to _Sidebar.md
    sidebar_path = wiki_path / "_Sidebar.md"
    final_markdown = "\n".join(sidebar_content) + "\n"
    
    try:
        with open(sidebar_path, 'w', encoding='utf-8') as f:
            f.write(final_markdown)
        print(f"[SUCCESS] _Sidebar.md successfully regenerated.")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] Failed to write _Sidebar.md: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()