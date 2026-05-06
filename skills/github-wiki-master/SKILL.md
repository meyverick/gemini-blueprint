---
name: github-wiki-master
description: Orchestrates GitHub wiki provisioning, semantic page validation, and synchronization via local git manipulation and automated sidebar generation.
---

# GitHub Wiki Master

## 1. Discovery Phase

Activate this skill when requested to structure, create, audit, or deploy comprehensive documentation to a GitHub repository's built-in Wiki.

**Target Environment Constraints:**

* GitHub Wikis are separate Git repositories (suffix: `.wiki.git`).
* Wikis do not natively support pull requests; changes are pushed directly to the `master` branch.
* Supported formats: Markdown (`.md`), MediaWiki (`.mediawiki`), AsciiDoc (`.asciidoc`). Default to `.md`.

## 2. Activation Phase

Before executing page creation, establish the local staging environment and validate access.

**Procedure:**

1. **Locate Target:** Identify the target repository `owner/repo`.
2. **Clone Wiki:** Execute `git clone https://github.com/<owner>/<repo>.wiki.git` into a local `/tmp/` staging directory.
3. **Verify Auth:** Ensure the environment has standard GitHub Git credentials loaded.
4. **Init Structure:** If the repository is empty, populate it using the defaults from `assets/templates/`.

## 3. Execution Phase

All modifications must occur locally, be subjected to static validation, and then pushed. Follow these strict procedural loops.

### Page Creation Loop

1. Generate the markdown file in the local `.wiki.git` directory.
2. Replace spaces in filenames with hyphens (e.g., `API-Reference.md`).
3. Apply standard GFM formatting.

### Validation Loop

Always run the offloaded Python validators before attempting a push to prevent dead links and navigation silos.

1. Run `python scripts/validate_links.py <path_to_wiki_dir>` to verify internal link integrity.
2. Run `python scripts/build_sidebar.py <path_to_wiki_dir>` to recursively index new pages and inject them into `_Sidebar.md`.

### Synchronization Loop

1. Execute `git status` to verify staged changes.
2. Execute `python scripts/sync_wiki.py <path_to_wiki_dir> "feat: update wiki pages"` to stage, commit, and cleanly push.

## 4. Environment Gotchas & Edge Cases

* **Link Case-Sensitivity:** GitHub wiki links are case-sensitive on Linux/Web but case-insensitive on macOS/Windows local file systems. Always use exact casing for internal links `[[My-Page]]`.
* **Sidebar Caching:** The `_Sidebar.md` file aggressively caches on the GitHub CDN. If updates do not visually appear, append a nominal whitespace character and re-push.
* **Image Hosting:** GitHub Wikis cannot host relative images effectively unless they are committed directly to the `.wiki.git` repo. Store images in an `/images` directory within the wiki repo and reference via `[[/images/my-diagram.png]]`.
* **Unsupported Extensions:** Raw HTML `<script>`, `<iframe>`, and embedded CSS will be aggressively sanitized and stripped by GitHub's rendering engine. Stick strictly to GFM.
