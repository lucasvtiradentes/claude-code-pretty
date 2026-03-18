from claudecodepretty.constants import INDENT
from claudecodepretty.handlers.base import ParseResult, ParserState


def handle_todo(inp: dict, state: ParserState, result: ParseResult):
    r = state.renderer
    result.add(f"\n{state.sp}{r.yellow('[Todo]')}\n")
    for todo in inp.get("todos", []):
        status = todo.get("status", "pending")
        text = todo.get("content", "")
        if status == "completed":
            mark = r.green("[x]")
        elif status == "in_progress":
            mark = r.orange("[~]")
        else:
            mark = r.dim("[ ]")
        result.add(f"{state.sp}{INDENT}{mark} {text}\n")
    result.add("\n")
