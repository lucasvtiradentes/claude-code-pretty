import subprocess
import sys

from claudecodepretty.handlers import ParserState
from claudecodepretty.parser import parse_json_line


def run_stream(args: list[str]) -> int:
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
