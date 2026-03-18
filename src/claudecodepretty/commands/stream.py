import subprocess
import sys

from claudecodepretty.constants import CLI_NAME
from claudecodepretty.handlers import ParserState
from claudecodepretty.parser import parse_json_line


def print_help():
    print(f"""{CLI_NAME} stream - Run claude with pretty output

Usage:
  {CLI_NAME} stream [claude-args...]

All arguments are forwarded to claude. These flags are added automatically:
  --print --verbose --dangerously-skip-permissions --output-format stream-json

Examples:
  {CLI_NAME} stream -p "explain this code"
  {CLI_NAME} stream -p "fix the bug" --model sonnet --max-turns 3
  {CLI_NAME} stream --resume""")


def run(args):
    if not args or "-h" in args or "--help" in args:
        print_help()
        sys.exit(0)

    cmd = [
        "claude",
        "--print",
        "--verbose",
        "--dangerously-skip-permissions",
        "--output-format",
        "stream-json",
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

    sys.exit(process.returncode)
