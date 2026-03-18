import os
import sys

from claudecodepretty.constants import CLI_NAME
from claudecodepretty.handlers import ParserState
from claudecodepretty.parser import parse_json_line


def print_help():
    print(f"""{CLI_NAME} show - Replay a saved session

Usage:
  {CLI_NAME} show <file.jsonl> [options]

Options:
  --browser          Open session in browser instead of terminal
  --port N           Port for browser server (default: 7860)

Examples:
  {CLI_NAME} show ~/.claude/projects/.../session.jsonl
  {CLI_NAME} show session.jsonl --browser --port 8080""")


def _parse_port(args):
    port = 7860
    if "--port" in args:
        idx = args.index("--port")
        try:
            port = int(args[idx + 1])
            args = args[:idx] + args[idx + 2 :]
        except (IndexError, ValueError):
            print("Error: --port requires a number")
            sys.exit(1)
    return port, args


def _replay(file_path):
    state = ParserState(mode="replay")

    r = state.renderer

    if file_path == "-":
        source = sys.stdin
        print(f"{r.dim('[replay] stdin')}\n")
    else:
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}")
            return 1
        source = open(file_path, "r")
        print(f"{r.dim(f'[replay] {file_path}')}\n")

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


def run(args):
    if not args or "-h" in args or "--help" in args:
        print_help()
        sys.exit(0)

    if "--browser" in args:
        args_clean = [a for a in args if a != "--browser"]
        port, args_clean = _parse_port(args_clean)

        if not args_clean:
            print("Error: show requires a file path")
            sys.exit(1)

        from claudecodepretty.commands.sessions.server import serve_session

        file_path = args_clean[0]
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}")
            sys.exit(1)
        sys.exit(serve_session(file_path, port))

    file_args = [a for a in args if not a.startswith("--")]
    if not file_args:
        print("Error: show requires a file path")
        sys.exit(1)

    sys.exit(_replay(file_args[0]))
