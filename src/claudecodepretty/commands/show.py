import os
import sys

from claudecodepretty.constants import CLI_NAME
from claudecodepretty.handlers import ParserState
from claudecodepretty.parser import parse_json_line


def print_help():
    print(f"""{CLI_NAME} show - Replay a saved session

Usage:
  {CLI_NAME} show <file.jsonl>

Examples:
  {CLI_NAME} show ~/.claude/projects/.../session.jsonl""")


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

    sys.exit(_replay(args[0]))
