import json

from claudecodepretty.colors import RED, RESET
from claudecodepretty.handlers import (
    ParseResult,
    ParserState,
    handle_assistant_message,
    handle_result,
    handle_stream_event,
    handle_system,
    handle_user_message,
)

__all__ = ["parse_json_line", "ParserState", "ParseResult"]


def parse_json_line(line: str, state: ParserState) -> ParseResult:
    result = ParseResult()

    try:
        data = json.loads(line)
    except json.JSONDecodeError:
        return result

    msg_type = data.get("type", "")

    if msg_type == "system":
        handle_system(data, state, result)
    elif msg_type == "stream_event":
        handle_stream_event(data, state, result)
    elif msg_type == "user":
        handle_user_message(data, state, result)
    elif msg_type == "assistant":
        handle_assistant_message(data, state, result)
    elif msg_type == "result":
        handle_result(data, state, result)
    elif msg_type == "error":
        result.add(f"\n{state.sp}{RED}[error] {data.get('error', 'unknown error')}{RESET}")

    return result
