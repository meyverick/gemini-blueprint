#!/usr/bin/env python3
import os
import re
import sys
import argparse
import urllib.parse
from pathlib import Path

def extract_links(file_path):
    """
    Parses a markdown file and extracts both standard MD links and GitHub Wiki links.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"ERROR: Could not read {file_path}: {e}")
        return [], []

    # Match Wiki links: [[Page-Name]] or [[Text|Page-Name]]
    wiki_links_raw = re.findall(r'\[\[(.*?)\]\]', content)
    parsed_wiki_links = []
    for wl in wiki_links_raw:
        # If piped, the target is on the right
        target = wl.split('|')[-1].strip()
        # Strip internal anchor tags for file resolution (e.g., [[Page#Section]])
        target = target.split('#')[0] 
        if target:
            parsed_wiki_links.append(target)

    # Match Standard markdown links: [Text](target)
    md_links_raw = re.findall(r'\[[^\]]*\]\(([^)]+)\)', content)
    parsed_md_links = []
    for ml in md_links_raw:
        # Unquote URL encoding and strip internal anchors
        target = urllib.parse.unquote(ml).split('#')[0].strip()
        # Ignore external links, mailto, and pure anchors
        if target and not target.startswith(('http://', 'https://', 'mailto:', 'ftp://')):
            parsed_md_links.append(target)

    return parsed_wiki_links, parsed_md_links

def main():
    parser = argparse.ArgumentParser(
        description="Static analyzer for GitHub Wiki markdown links. Returns exit code 1 if dead links are found."
    )
    parser.add_argument("wiki_dir", type=str, help="Absolute or relative path to the local .wiki.git directory")
    args = parser.parse_args()

    wiki_path = Path(args.wiki_dir).resolve()
    
    if not wiki_path.is_dir():
        print(f"FATAL: Directory '{wiki_path}' does not exist.")
        sys.exit(1)

    # 1. Map existing valid destinations
    # GitHub wikis resolve pages by their filename stem (without .md)
    existing_pages = {}
    for root, dirs, files in os.walk(wiki_path):
        if '.git' in dirs:
            dirs.remove('.git')  # Ignore git internals
        
        for file in files:
            if file.endswith('.md'):
                rel_path = Path(root).joinpath(file).relative_to(wiki_path)
                page_name = rel_path.stem
                # Map lowercase version for case-insensitive lookup, store actual case to warn about mismatches
                existing_pages[page_name.lower()] = page_name

    errors = 0
    warnings = 0
    
    # 2. Traverse and validate
    for root, dirs, files in os.walk(wiki_path):
        if '.git' in dirs:
            dirs.remove('.git')
            
        for file in files:
            if not file.endswith('.md'):
                continue
                
            file_path = Path(root).joinpath(file)
            rel_file_path = file_path.relative_to(wiki_path)
            
            wiki_links, md_links = extract_links(file_path)
            
            # Validate [[Wiki Links]]
            for target in wiki_links:
                # GitHub wiki maps spaces to hyphens internally
                target_canonical = target.replace(' ', '-').lower()
                
                if target_canonical not in existing_pages:
                    print(f"[ERROR] DEAD WIKI LINK : '[[{target}]]' inside {rel_file_path}")
                    errors += 1
                elif existing_pages[target_canonical] != target.replace(' ', '-'):
                    print(f"[WARN]  CASE MISMATCH  : '[[{target}]]' inside {rel_file_path} -> resolves to '{existing_pages[target_canonical]}.md'. May break on Linux environments.")
                    warnings += 1

            # Validate [Standard](Links)
            for target in md_links:
                # Strip '.md' if present to check against wiki page dictionary
                if target.lower().endswith('.md'):
                    target_stem = Path(target).stem.lower()
                else:
                    target_stem = target.replace(' ', '-').lower()

                if target_stem not in existing_pages:
                    # Fallback: check if it references a static file (e.g., /images/diagram.png)
                    # Resolve relative to the current file's directory or from repo root if starts with /
                    if target.startswith('/'):
                        target_path = (wiki_path / target.lstrip('/')).resolve()
                    else:
                        target_path = (file_path.parent / target).resolve()
                        
                    if not target_path.exists():
                        print(f"[ERROR] DEAD FILE LINK : '[...]({target})' inside {rel_file_path}")
                        errors += 1

    # 3. Execution Gateway
    print(f"\n--- Validation Summary ---")
    print(f"Pages Scanned: {len(existing_pages)}")
    print(f"Warnings: {warnings}")
    print(f"Errors: {errors}")
    
    if errors > 0:
        print("\nSTATUS: FAILED. Please correct dead links before pushing.")
        sys.exit(1)
    else:
        print("\nSTATUS: PASS. All intra-wiki references are structurally sound.")
        sys.exit(0)

if __name__ == "__main__":
    main()