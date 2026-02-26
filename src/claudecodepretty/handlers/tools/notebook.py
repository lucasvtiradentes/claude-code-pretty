from claudecodepretty.colors import ORANGE, RESET
from claudecodepretty.handlers.base import ParseResult, ParserState


def handle_notebook(inp: dict, state: ParserState, result: ParseResult):
    result.add(f"\n{state.sp}{ORANGE}[NotebookEdit] {inp.get('notebook_path', '')}{RESET}\n")
