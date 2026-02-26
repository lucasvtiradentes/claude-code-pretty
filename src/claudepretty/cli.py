import os
import subprocess
import sys

from claudepretty import __version__
from claudepretty.colors import DIM, RESET
from claudepretty.constants import CLI_NAME
from claudepretty.parser import ParserState, parse_json_line


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


def run_stream(args: list[str]):
    cmd = [
        "claude",
        "--print",
        "--verbose",
        "--dangerously-skip-permissions",
        "--output-format", "stream-json",
        "--include-partial-messages",
        *args,
    ]

    state = ParserState(mode="stream")

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    try:
        for line in process.stdout:
            line = line.strip()
            if line:
                result = parse_json_line(line, state)
                output = result.get_output()
                if output:
                    print(output, end="", flush=True)
    except KeyboardInterrupt:
        process.terminate()
        sys.exit(130)
    finally:
        process.wait()

    return process.returncode


def run_replay(file_path: str):
    state = ParserState(mode="replay")

    if file_path == "-":
        source = sys.stdin
        print(f"{DIM}[replay] stdin{RESET}\n")
    else:
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}")
            return 1
        source = open(file_path, "r")
        print(f"{DIM}[replay] {file_path}{RESET}\n")

    try:
        for line in source:
            line = line.strip()
            if line:
                result = parse_json_line(line, state)
                output = result.get_output()
                if output:
                    print(output, end="", flush=True)
    finally:
        if file_path != "-":
            source.close()

    return 0


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
