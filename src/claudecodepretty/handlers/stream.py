from claudecodepretty.constants import HIDE_TOOLS
from claudecodepretty.handlers.base import ParseResult, ParserState


def handle_stream_event(data: dict, state: ParserState, result: ParseResult):
    r = state.renderer
    event = data.get("event", {})
    event_type = event.get("type", "")

    if event_type == "content_block_start":
        if state.subagent_depth > 0:
            result.add(f"{state.sp}{r.section_close()}\n")
            state.decrement_depth()

        block = event.get("content_block", {})
        if block.get("type") == "tool_use":
            name = block.get("name", "")
            state.current_tool = name
            if name not in HIDE_TOOLS:
                result.add(f"\n{state.sp}{r.purple(f'[{name}]')} ")

    elif event_type == "content_block_delta":
        delta = event.get("delta", {})
        delta_type = delta.get("type", "")

        if delta_type == "text_delta":
            result.add(state.render_text(delta.get("text", "")))
        elif delta_type == "input_json_delta":
            if state.current_tool not in HIDE_TOOLS:
                result.add(delta.get("partial_json", ""))

    elif event_type == "content_block_stop":
        if state.current_tool not in HIDE_TOOLS:
            result.add(f"{r.style_reset()}\n")
        state.current_tool = ""

    elif event_type == "error":
        error = event.get("error", str(event))
        result.add(f"\n{state.sp}{r.red(f'[error] {error}')}\n")
