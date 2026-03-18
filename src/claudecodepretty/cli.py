import sys

from claudecodepretty import __version__
from claudecodepretty.constants import CLI_NAME


def print_help():
    print(f"""{CLI_NAME} - Pretty formatter for Claude Code stream-json output

Usage:
  {CLI_NAME} <command> [options]

Commands:
  stream [claude-args...]          Run claude with pretty output (forwards all args)
  show <file.jsonl>                Replay a saved session (.jsonl)

Options:
  -h, --help         Show this help
  -v, --version      Show version

Environment:
  CP_TOOL_RESULT_MAX_CHARS   Max chars for tool results (default: 300, 0=hide)
  CP_READ_PREVIEW_LINES      Lines to preview from Read (default: 5, 0=hide)

Examples:
  {CLI_NAME} stream -p "explain this code"
  {CLI_NAME} show ~/.claude/projects/.../session.jsonl""")


COMMANDS = {
    "stream": "claudecodepretty.commands.stream",
    "show": "claudecodepretty.commands.show",
}


def main():
    args = sys.argv[1:]

    if not args or "-h" in args or "--help" in args:
        print_help()
        sys.exit(0)

    if "-v" in args or "--version" in args:
        print(__version__)
        sys.exit(0)

    command = args[0]
    sub_args = args[1:]

    if command not in COMMANDS:
        print(f"Unknown command: {command}")
        print(f"Run '{CLI_NAME} --help' for usage")
        sys.exit(1)

    from importlib import import_module

    mod = import_module(COMMANDS[command])
    mod.run(sub_args)


if __name__ == "__main__":
    main()
