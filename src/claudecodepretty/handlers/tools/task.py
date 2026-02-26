from claudecodepretty.colors import BLUE, DIM, RESET
from claudecodepretty.handlers.base import ParseResult, ParserState


def handle_task(inp: dict, state: ParserState, result: ParseResult):
    prompt = inp.get("prompt", inp.get("description", ""))[:50]
    model = inp.get("model", "sonnet")
    result.add(f'\n{state.sp}{BLUE}[Task] "{prompt}" ({model}){RESET}\n')
    if state.mode == "stream":
        state.increment_depth()
        result.add(f"{state.sp}{DIM}┌───────────────────────────────{RESET}\n")
