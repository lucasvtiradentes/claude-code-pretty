from claudecodepretty.handlers.base import ParseResult, ParserState


def handle_glob(inp: dict, state: ParserState, result: ParseResult):
    r = state.renderer
    pattern = inp.get("pattern", "")
    result.add(f"\n{state.sp}{r.purple(f'[Glob] {pattern}')}\n")
