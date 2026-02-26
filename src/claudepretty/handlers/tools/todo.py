from claudepretty.colors import DIM, GREEN, ORANGE, RESET, YELLOW
from claudepretty.constants import INDENT
from claudepretty.handlers.base import ParseResult, ParserState


def handle_todo(inp: dict, state: ParserState, result: ParseResult):
    result.add(f"\n{state.sp}{YELLOW}[Todo]{RESET}\n")
    for todo in inp.get("todos", []):
        status = todo.get("status", "pending")
        text = todo.get("content", "")
        if status == "completed":
            mark = f"{GREEN}[x]{RESET}"
        elif status == "in_progress":
            mark = f"{ORANGE}[~]{RESET}"
        else:
            mark = f"{DIM}[ ]{RESET}"
        result.add(f"{state.sp}{INDENT}{mark} {text}\n")
    result.add("\n")
