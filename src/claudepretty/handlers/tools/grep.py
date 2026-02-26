from claudepretty.colors import PURPLE, RESET
from claudepretty.handlers.base import ParseResult, ParserState


def handle_grep(inp: dict, state: ParserState, result: ParseResult):
    pattern = inp.get("pattern", "")
    path = inp.get("path", "")
    if path:
        path = path.split("/")[-1]
        result.add(f'\n{state.sp}{PURPLE}[Grep] "{pattern}" in {path}{RESET}\n')
    else:
        result.add(f'\n{state.sp}{PURPLE}[Grep] "{pattern}"{RESET}\n')
