from claudecodepretty.handlers.base import ParseResult, ParserState


def handle_task(inp: dict, state: ParserState, result: ParseResult):
    r = state.renderer
    prompt = inp.get("prompt", inp.get("description", ""))[:50]
    model = inp.get("model", "sonnet")
    label = f'[Task] "{prompt}" ({model})'
    result.add(f"\n{state.sp}{r.blue(label)}\n")
    if state.mode == "stream":
        state.increment_depth()
        result.add(f"{state.sp}{r.section_open()}\n")
