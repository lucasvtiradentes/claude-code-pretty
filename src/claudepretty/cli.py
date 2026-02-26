import sys

from claudepretty import __version__
from claudepretty.constants import CLI_NAME
from claudepretty.modes import run_replay, run_stream


def print_help():
    print(f"""{CLI_NAME} - Pretty formatter for Claude Code stream-json output

Usage:
  {CLI_NAME} [OPTIONS] [CLAUDE_ARGS...]
  {CLI_NAME} -f <session.jsonl>

Options:
  -f, --file FILE    Replay a saved session .jsonl file
  -h, --help         Show this help
  -v, --version      Show version

Environment:
  CP_TOOL_RESULT_MAX_CHARS   Max chars for tool results (default: 300, 0=hide)
  CP_READ_PREVIEW_LINES      Lines to preview from Read (default: 5, 0=hide)

Examples:
  {CLI_NAME} -p "explain this code"
  {CLI_NAME} -f ~/.claude/projects/.../session.jsonl
  cat session.jsonl | {CLI_NAME} -f -""")


def main():
    args = sys.argv[1:]

    if not args or "-h" in args or "--help" in args:
        print_help()
        sys.exit(0)

    if "-v" in args or "--version" in args:
        print(__version__)
        sys.exit(0)

    if "-f" in args or "--file" in args:
        try:
            idx = args.index("-f") if "-f" in args else args.index("--file")
            file_path = args[idx + 1]
            sys.exit(run_replay(file_path))
        except IndexError:
            print("Error: -f requires a file path")
            sys.exit(1)

    sys.exit(run_stream(args))


if __name__ == "__main__":
    main()
