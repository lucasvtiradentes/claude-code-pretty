from claudecodepretty.colors import render_markdown
from claudecodepretty.handlers.base import ParseResult, ParserState
from claudecodepretty.handlers.tools import dispatch_tool


def handle_assistant_message(data: dict, state: ParserState, result: ParseResult):
    message = data.get("message", {})
    content = message.get("content", [])

    if not isinstance(content, list):
        return

    if state.mode == "replay":
        for block in content:
            if block.get("type") == "text":
                result.add(render_markdown(block.get("text", "")))

    for block in content:
        if block.get("type") != "tool_use":
            continue

        name = block.get("name", "")
        inp = block.get("input", {})
        dispatch_tool(name, inp, state, result)
