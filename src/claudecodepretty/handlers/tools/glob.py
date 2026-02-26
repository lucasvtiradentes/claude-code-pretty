from claudecodepretty.colors import PURPLE, RESET
from claudecodepretty.handlers.base import ParseResult, ParserState


def handle_glob(inp: dict, state: ParserState, result: ParseResult):
    result.add(f"\n{state.sp}{PURPLE}[Glob] {inp.get('pattern', '')}{RESET}\n")
