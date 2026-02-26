import os
import sys

from claudecodepretty.colors import DIM, RESET
from claudecodepretty.handlers import ParserState
from claudecodepretty.parser import parse_json_line


def run_replay(file_path: str) -> int:
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
