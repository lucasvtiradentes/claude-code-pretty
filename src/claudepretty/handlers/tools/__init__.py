from claudepretty.handlers.base import ParseResult, ParserState
from claudepretty.handlers.tools.bash import handle_bash
from claudepretty.handlers.tools.edit import handle_edit
from claudepretty.handlers.tools.glob import handle_glob
from claudepretty.handlers.tools.grep import handle_grep
from claudepretty.handlers.tools.notebook import handle_notebook
from claudepretty.handlers.tools.read import handle_read
from claudepretty.handlers.tools.task import handle_task
from claudepretty.handlers.tools.todo import handle_todo
from claudepretty.handlers.tools.write import handle_write


def dispatch_tool(name: str, inp: dict, state: ParserState, result: ParseResult):
    if name == "TodoWrite":
        handle_todo(inp, state, result)
    elif name == "Write":
        handle_write(inp, state, result)
    elif name == "Read":
        handle_read(inp, state, result)
    elif name == "Glob":
        handle_glob(inp, state, result)
    elif name == "Grep":
        handle_grep(inp, state, result)
    elif name in ("Edit", "MultiEdit"):
        handle_edit(name, inp, state, result)
    elif name == "NotebookEdit":
        handle_notebook(inp, state, result)
    elif name == "Bash":
        handle_bash(inp, state, result)
    elif name == "Task":
        handle_task(inp, state, result)
