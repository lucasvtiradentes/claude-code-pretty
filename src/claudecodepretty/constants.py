import os

CLI_NAME = "claudep"
DIST_NAME = "claude-code-pretty"
INDENT = "   "
HIDE_TOOLS = {"Write", "TodoWrite", "Read", "Glob", "Grep", "Bash", "Task", "Edit", "MultiEdit", "NotebookEdit"}

TOOL_RESULT_MAX_CHARS = int(os.environ.get("CP_TOOL_RESULT_MAX_CHARS", "300"))
READ_PREVIEW_LINES = int(os.environ.get("CP_READ_PREVIEW_LINES", "5"))
