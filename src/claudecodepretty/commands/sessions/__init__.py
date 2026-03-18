import sys

from claudecodepretty.constants import CLI_NAME


def print_help():
    print(f"""{CLI_NAME} sessions - Browse all sessions in browser

Usage:
  {CLI_NAME} sessions [options]

Options:
  --port N           Port for browser server (default: 7860)""")


def run(args):
    if "-h" in args or "--help" in args:
        print_help()
        sys.exit(0)

    port = 7860
    if "--port" in args:
        idx = args.index("--port")
        try:
            port = int(args[idx + 1])
        except (IndexError, ValueError):
            print("Error: --port requires a number")
            sys.exit(1)

    print(f"Sessions browser not yet implemented (port={port})")
    sys.exit(1)
