from claudecodepretty.colors import PURPLE, RESET
from claudecodepretty.handlers.base import ParseResult, ParserState


def handle_bash(inp: dict, state: ParserState, result: ParseResult):
    result.add(f"\n{state.sp}{PURPLE}[Bash] {inp.get('command', '')}{RESET}\n")
