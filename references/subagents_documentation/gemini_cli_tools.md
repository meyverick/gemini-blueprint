# Available Gemini CLI tools

- Activate Skill (activate_skill): Activates a specialized agent skill by name (Available: 'skill-creator'). Returns the skill's instructions wrapped in <activated_skill> tags. These provide specialized guidance for the current task. Use this when you identify a task that matches a skill's description. ONLY use names exactly as they appear in the <available_skills> section.
- Ask User (ask_user): Ask the user one or more questions to gather preferences, clarify requirements, or make decisions.
- CLI Help Agent (cli_help): Specialized agent for answering questions about the Gemini CLI application. Invoke this agent for questions regarding CLI features, configuration schemas (e.g., policies), or instructions on how to create custom subagents. It queries internal documentation to provide accurate usage guidance.
- Codebase Investigator Agent (codebase_investigator): The specialized tool for codebase analysis, architectural mapping, and understanding system-wide dependencies. Invoke this tool for tasks like vague requests, bug root-cause analysis, system refactoring, comprehensive feature implementation or to answer questions about the codebase that require investigation. It returns a structured report with key file paths, symbols, and actionable architectural insights.
- Edit (replace): Replaces text within a file. By default, the tool expects to find and replace exactly ONE occurrence of old_string. If you want to replace multiple occurrences of the exact same string, set allow_multiple to true. This tool requires providing significant context around the change to ensure precise targeting. Always use the read_file tool to examine the file's current content before attempting a text replacement. The user has the ability to modify the new_string content. If modified, this will be stated in the response.
  - Expectation for required parameters:
    1. old_string MUST be the exact literal text to replace (including all whitespace, indentation, newlines, and surrounding code etc.).
    2. new_string MUST be the exact literal text to replace old_string with (also including all whitespace, indentation, newlines, and surrounding code etc.). Ensure the resulting code is correct and idiomatic and that old_string and new_string are different.
    3. instruction is the detailed instruction of what needs to be changed. It is important to Make it specific and detailed so developers or large language models can understand what needs to be changed and perform the changes on their own if necessary.
    4. NEVER escape old_string or new_string, that would break the exact literal text requirement.

    **Important:** If ANY of the above are not satisfied, the tool will fail. CRITICAL for old_string: Must uniquely identify the instance(s) to change. Include at least 3 lines of context BEFORE and AFTER the target text, matching whitespace and indentation precisely. If this string matches multiple locations and allow_multiple is not true, the tool will fail.

    5. Prefer to break down complex and long changes into multiple smaller atomic calls to this tool. Always check the content of the file after changes or not finding a string to match.

    **Multiple replacements:** Set allow_multiple to true if you want to replace ALL occurrences that match old_string exactly.

- FindFiles (glob): Efficiently finds files matching specific glob patterns (e.g., src/**/*.ts, **/*.md), returning absolute paths sorted by modification time (newest first). Ideal for quickly locating files based on their name or path structure, especially in large codebases.
- Generalist Agent (generalist): A general-purpose AI agent with access to all tools. Highly recommended for tasks that are turn-intensive or involve processing large amounts of data. Use this to keep the main session history lean and efficient. Excellent for: batch refactoring/error fixing across multiple files, running commands with high-volume output, and speculative investigations.
- GoogleSearch (google_web_search): Performs a web search using Google Search (via the Gemini API) and returns the results. This tool is useful for finding information on the internet based on a query.
- Memory Manager (save_memory): Writes and reads memory, preferences or facts across ALL future sessions. Use this for recurring instructions like coding styles or tool aliases.
- MCP Server (`mcp_*` or `mcp_{serverName}_*` or `mcp_{serverName}_{toolName}`): Connects to an MCP server to access additional tools and capabilities.
- ReadFile (read_file): Reads and returns the content of a specified file. If the file is large, the content will be truncated. The tool's response will clearly indicate if truncation has occurred and will provide details on how to read more of the file using the 'start_line' and 'end_line' parameters. Handles text, images (PNG, JPG, GIF, WEBP, SVG, BMP), audio files (MP3, WAV, AIFF, AAC, OGG, FLAC), and PDF files. For text files, it can read specific line ranges.
- ReadFolder (list_directory): Lists the names of files and subdirectories directly within a specified directory path. Can optionally ignore entries matching provided glob patterns.
- SearchText (grep_search): Searches for a regular expression pattern within file contents.
- Shell (run_shell_command): This tool executes a given shell command as `bash -c <command>`. To run a command in the background, set the is_background parameter to true. Do NOT use & to background commands. Command is executed as a subprocess that leads its own process group. Command process group can be terminated as kill -- -PGID or signaled as kill -s SIGNAL -- -PGID.

**Efficiency Guidelines:**

- Quiet Flags: Always prefer silent or quiet flags (e.g., npm install --silent, git --no-pager) to reduce output volume while still capturing necessary information.
- Pagination: Always disable terminal pagination to ensure commands terminate (e.g., use git --no-pager, systemctl --no-pager, or set PAGER=cat).

**The following information is returned:**

- Output: Combined stdout/stderr. Can be (empty) or partial on error and for any unwaited background processes.
- Exit Code: Only included if non-zero (command failed).
- Error: Only included if a process-level error occurred (e.g., spawn failure).
- Signal: Only included if process was terminated by a signal.
- Background PIDs: Only included if background processes were started.
- Process Group PGID: Only included if available.

- WebFetch (web_fetch): Processes content from URL(s), including local and private network addresses (e.g., localhost), embedded in a prompt. Include up to 20 URLs and instructions (e.g., summarize, extract specific data) directly in the 'prompt' parameter.
- WriteFile (write_file): Writes content to a specified file in the local filesystem.

The user has the ability to modify the new_string content. If modified, this will be stated in the response.
