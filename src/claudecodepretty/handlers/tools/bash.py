from claudecodepretty.handlers.base import ParseResult, ParserState


def handle_bash(inp: dict, state: ParserState, result: ParseResult):
    r = state.renderer
    cmd = inp.get("command", "")
    result.add(f"\n{state.sp}{r.purple(f'[Bash] {cmd}')}\n")
