from claudepretty.colors import ORANGE, RESET
from claudepretty.handlers.base import ParseResult, ParserState


def handle_write(inp: dict, state: ParserState, result: ParseResult):
    result.add(f"\n{state.sp}{ORANGE}[Write] {inp.get('file_path', '')}{RESET}\n")
