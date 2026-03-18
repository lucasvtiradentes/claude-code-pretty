from claudecodepretty.handlers.base import ParseResult, ParserState


def handle_read(inp: dict, state: ParserState, result: ParseResult):
    r = state.renderer
    path = inp.get("file_path", "")
    result.add(f"\n{state.sp}{r.green(f'[Read] {path}')}\n")
