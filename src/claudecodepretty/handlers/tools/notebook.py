from claudecodepretty.handlers.base import ParseResult, ParserState


def handle_notebook(inp: dict, state: ParserState, result: ParseResult):
    r = state.renderer
    path = inp.get("notebook_path", "")
    result.add(f"\n{state.sp}{r.orange(f'[NotebookEdit] {path}')}\n")
