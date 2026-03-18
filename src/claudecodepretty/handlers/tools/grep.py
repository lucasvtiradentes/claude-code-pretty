from claudecodepretty.handlers.base import ParseResult, ParserState


def handle_grep(inp: dict, state: ParserState, result: ParseResult):
    r = state.renderer
    pattern = inp.get("pattern", "")
    path = inp.get("path", "")
    if path:
        path = path.split("/")[-1]
        label = f'[Grep] "{pattern}" in {path}'
    else:
        label = f'[Grep] "{pattern}"'
    result.add(f"\n{state.sp}{r.purple(label)}\n")
