import re

from claudepretty.colors import CYAN, DIM, GREEN, RED, RESET
from claudepretty.constants import INDENT, READ_PREVIEW_LINES, TOOL_RESULT_MAX_CHARS
from claudepretty.handlers.base import ParseResult, ParserState


def handle_user_message(data: dict, state: ParserState, result: ParseResult):
    message = data.get("message", {})
    content = message.get("content", "")

    if isinstance(content, str):
        if state.mode == "replay":
            text = content[:200]
            result.add(f"\n{GREEN}[user]{RESET} {text}")
            if len(content) > 200:
                result.add(f"{DIM}...{RESET}")
            result.add("\n")
        return

    if not isinstance(content, list) or not content:
        return

    first = content[0]
    content_type = first.get("type", "")

    if content_type == "tool_result":
        tool_content = first.get("content", "")

        if isinstance(tool_content, str):
            if tool_content.startswith(("Todos have been", "The file")) and "has been" in tool_content:
                return
            if "<tool_use_error>" in tool_content:
                error_msg = re.sub(r"<[^>]*>", "", tool_content)
                result.add(f"{state.sp}{RED}{INDENT}✗ {error_msg}{RESET}\n\n")
                return

            if "\n" in tool_content:
                if READ_PREVIEW_LINES == 0:
                    return
                lines = tool_content.split("\n")[:READ_PREVIEW_LINES]
                for line in lines:
                    result.add(f"{state.sp}{CYAN}{INDENT}→ {line}{RESET}\n")
                if len(tool_content.split("\n")) > READ_PREVIEW_LINES:
                    result.add(f"{state.sp}{INDENT}...\n")
                result.add("\n")
            else:
                if TOOL_RESULT_MAX_CHARS == 0:
                    return
                text = tool_content if TOOL_RESULT_MAX_CHARS < 0 else tool_content[:TOOL_RESULT_MAX_CHARS]
                result.add(f"{state.sp}{CYAN}{INDENT}→ {text}{RESET}\n\n")
