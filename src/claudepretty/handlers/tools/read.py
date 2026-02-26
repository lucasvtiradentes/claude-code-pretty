from claudepretty.colors import GREEN, RESET
from claudepretty.handlers.base import ParseResult, ParserState


def handle_read(inp: dict, state: ParserState, result: ParseResult):
    result.add(f"\n{state.sp}{GREEN}[Read] {inp.get('file_path', '')}{RESET}\n")
