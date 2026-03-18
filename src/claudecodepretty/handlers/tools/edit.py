from claudecodepretty.handlers.base import ParseResult, ParserState


def handle_edit(name: str, inp: dict, state: ParserState, result: ParseResult):
    r = state.renderer
    path = inp.get("file_path", "")
    result.add(f"\n{state.sp}{r.orange(f'[{name}] {path}')}\n")
