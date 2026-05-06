# Repository Maintenance

The Gemini Blueprint Workspace includes automated utilities for repository synchronization.

## Repository Synchronization

Bulk synchronization of repositories located in `references/repositories/` is managed via `update_repos.py`.

### Features
- **Existing Repository Sync**: Iterates through subdirectories in the target path and updates any detected Git repositories.
- **Dirty State Protection**: Skips repositories with uncommitted changes to prevent data loss or merge conflicts.
- **Fast-Forward Updates**: Performs non-destructive `git pull --ff-only` with pruning to ensure local branches remain synchronized with origin.
- **Plain Text Fidelity**: Employs a zero-colorization strategy, utilizing high-fidelity emoji indicators for visual feedback in plain text environments.

### Usage
```powershell
python update_repos.py
```
