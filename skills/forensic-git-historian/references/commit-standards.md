# Commit Standards: The Forensic Ledger

## 1. The Epistemological Ruleset
| Rule | Specification |
| :--- | :--- |
| **Separation** | Separate the subject line from the body with exactly one blank line. |
| **Length** | Limit the subject line to 50 characters or fewer. |
| **Casing** | Capitalize the first letter of the subject line. |
| **Punctuation** | The subject line MUST NOT end with a period. |
| **Mood** | Use the imperative mood (e.g., "Add feature"). Complete: "If applied, the commit will...". |
| **Wrapping** | Wrap the body of the commit message at exactly 72 characters. |
| **Rationale** | The body documents the "Why" and "What", never the "How". |
| **Style** | Place periods and commas outside quotation marks unless part of the original quote. |

## 2. Conventional Commits v1.0.0
| Type | Semantic Meaning | SemVer Impact |
| :--- | :--- | :--- |
| **feat** | A new feature | MINOR |
| **fix** | A bug fix | PATCH |
| **docs** | Documentation-only changes | NONE |
| **style** | Formatting, white-space, linting (non-functional) | NONE |
| **refactor** | Code changes that neither fix a bug nor add a feature | NONE |
| **perf** | Code changes that improve performance | NONE |
| **test** | Addition/Correction of tests | NONE |
| **build** | Build system or external dependency changes | NONE |
| **ci** | CI configuration/script changes | NONE |
| **chore** | Maintenance tasks (e.g., .gitignore updates) | NONE |
| **revert** | Reversal of a previous commit | VARIES |

**Format:** `<type>(<scope>)<!>: <description>`
- **Scope:** Optional noun identifying the subsystem (e.g., `parser`, `auth`). Lowercase only.
- **Breaking Change:** Append `!` after type/scope and use `BREAKING CHANGE:` footer.

## 3. Security & Integrity Mandate (The "Watchtower" Step)
Before any commit is finalized, the **Forensic Git Historian** must audit the `.gitignore` configuration to prevent data leaks.

| Check | Objective |
| :--- | :--- |
| **Sensitive Exclusions** | Verify that `.env`, `.pem`, `.key`, and credential files are explicitly ignored. |
| **Build Artifacts** | Ensure `node_modules`, `dist`, `build`, and platform-specific binaries (e.g., `.apk`, `.exe`) are excluded. |
| **Workspace Metadata** | Confirm that `.vscode`, `.idea`, and local configuration folders are ignored to prevent environment drift. |
| **Staged Verification** | Cross-reference `git status` output against `.gitignore` to ensure no sensitive files are accidentally tracked or staged. |

## 4. Post-Commit Synchronization Mandate
To maintain the **Epistemological Ledger's** integrity, the project `changelog.md` must be updated immediately following a successful commit.

| Action | Mandate |
| :--- | :--- |
| **Trigger** | After `git commit` execution succeeds. |
| **Delegation** | Invoke the **changelog-architect** skill. |
| **Verification** | Ensure the new commit is reflected in the `## [Unreleased]` or latest version section. |

## 5. Metadata & Trailers
- **Separator:** Footers follow the body, separated by a blank line.
- **Syntax:** `Token: <value>` or `Token #<value>`.
- **Token Formatting:** Hyphenate tokens (e.g., `Refs-to:`, `Co-authored-by:`).
- **Issue Reference:** Use `Refs: #123` or `Closes: #123`.

## 6. Boundary Enforcement (Negative Constraints)
- **NO SYNTAX DESCRIPTION:** Do not describe code syntax (e.g., "Add if statement"). Describe the logic.
- **NO GENERIC SUBJECTS:** Never use "Update code", "Fix bug", or "Work in progress".
- **NO PLACEHOLDERS:** Never include "unchanged code" or "..." in any description.
- **NO AMBIGUOUS PRONOUNS:** Ensure maximum lexical density via noun repetition. Eradicate "it", "this", and "they".
- **NO TRAILING PERIODS:** Ensure the subject line ends without a period.

## 7. Final Quality Assurance Checklist
- [ ] Subject line is ≤ 50 characters, capitalized, and in imperative mood.
- [ ] Subject line has NO trailing period.
- [ ] Body lines are wrapped at exactly 72 characters.
- [ ] Periods and commas are placed OUTSIDE quotation marks.
- [ ] Zero-Pronoun Policy is strictly applied (no "it", "this", "they").
- [ ] **.gitignore Security Audit** is complete and no sensitive files are staged.
- [ ] **Changelog Sync** is planned as a post-commit action.
- [ ] Technical Rationale (Why) is clearly articulated in the body.
- [ ] Conventional Commit type is strictly correct.
- [ ] Output is wrapped in `<commit_message>` tags.
