import json
from dataclasses import dataclass, field
from typing import Any

from claudepretty.colors import BLUE, CYAN, DIM, GREEN, ORANGE, PURPLE, RED, RESET, YELLOW
from claudepretty.constants import FILE_LINES, HIDE_TOOLS, INDENT, RESULT_LIMIT


@dataclass
class ParserState:
    mode: str = "stream"
    current_tool: str = ""
    subagent_depth: int = 0
    sp: str = ""

    def update_sp(self):
        self.sp = "".join(f"{DIM}│{RESET} " for _ in range(self.subagent_depth))

    def increment_depth(self):
        self.subagent_depth += 1
        self.update_sp()

    def decrement_depth(self):
        if self.subagent_depth > 0:
            self.subagent_depth -= 1
            self.update_sp()


@dataclass
class ParseResult:
    output: str = ""
    messages: list[str] = field(default_factory=list)

    def add(self, text: str):
        self.messages.append(text)

    def add_inline(self, text: str):
        self.messages.append(text)

    def get_output(self) -> str:
        return "".join(self.messages)


def parse_json_line(line: str, state: ParserState) -> ParseResult:
    result = ParseResult()

    try:
        data = json.loads(line)
    except json.JSONDecodeError:
        return result

    msg_type = data.get("type", "")

    if msg_type == "system":
        _handle_system(data, state, result)
    elif msg_type == "stream_event":
        _handle_stream_event(data, state, result)
    elif msg_type == "user":
        _handle_user_message(data, state, result)
    elif msg_type == "assistant":
        _handle_assistant_message(data, state, result)
    elif msg_type == "result":
        _handle_result(data, state, result)
    elif msg_type == "error":
        result.add(f"\n{state.sp}{RED}[error] {data.get('error', 'unknown error')}{RESET}")

    return result


def _handle_system(data: dict, state: ParserState, result: ParseResult):
    if data.get("subtype") == "init":
        session_id = data.get("session_id", "")
        cwd = data.get("cwd", "").replace("/", "-").replace("_", "-")
        model = data.get("model", "")
        model_name = model.split("-")[1] if "-" in model else model

        result.add(f"{DIM}[session]\n")
        result.add(f"{INDENT}id:    {session_id}\n")
        result.add(f"{INDENT}path:  ~/.claude/projects/{cwd}/{session_id}.jsonl\n")
        result.add(f"{INDENT}model: {model_name}{RESET}\n\n")


def _handle_stream_event(data: dict, state: ParserState, result: ParseResult):
    event = data.get("event", {})
    event_type = event.get("type", "")

    if event_type == "content_block_start":
        if state.subagent_depth > 0:
            result.add(f"{state.sp}{DIM}└───────────────────────────────{RESET}\n")
            state.decrement_depth()

        block = event.get("content_block", {})
        if block.get("type") == "tool_use":
            name = block.get("name", "")
            state.current_tool = name
            if name not in HIDE_TOOLS:
                result.add(f"\n{state.sp}{PURPLE}[{name}] ")

    elif event_type == "content_block_delta":
        delta = event.get("delta", {})
        delta_type = delta.get("type", "")

        if delta_type == "text_delta":
            result.add_inline(delta.get("text", ""))
        elif delta_type == "input_json_delta":
            if state.current_tool not in HIDE_TOOLS:
                result.add_inline(delta.get("partial_json", ""))

    elif event_type == "content_block_stop":
        if state.current_tool not in HIDE_TOOLS:
            result.add(f"{RESET}\n")
        state.current_tool = ""

    elif event_type == "error":
        error = event.get("error", str(event))
        result.add(f"\n{state.sp}{RED}[error] {error}{RESET}\n")


def _handle_user_message(data: dict, state: ParserState, result: ParseResult):
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
                import re
                error_msg = re.sub(r"<[^>]*>", "", tool_content)
                result.add(f"{state.sp}{RED}{INDENT}✗ {error_msg}{RESET}\n\n")
                return

            if "\n" in tool_content:
                lines = tool_content.split("\n")[:10]
                for line in lines:
                    result.add(f"{state.sp}{CYAN}{INDENT}→ {line}{RESET}\n")
                if len(tool_content.split("\n")) > 10:
                    result.add(f"{state.sp}{INDENT}...\n")
                result.add("\n")
            else:
                result.add(f"{state.sp}{CYAN}{INDENT}→ {tool_content[:RESULT_LIMIT]}{RESET}\n\n")


def _handle_assistant_message(data: dict, state: ParserState, result: ParseResult):
    message = data.get("message", {})
    content = message.get("content", [])

    if not isinstance(content, list):
        return

    if state.mode == "replay":
        for block in content:
            if block.get("type") == "text":
                result.add(block.get("text", ""))

    for block in content:
        if block.get("type") != "tool_use":
            continue

        name = block.get("name", "")
        inp = block.get("input", {})

        if name == "TodoWrite":
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

        elif name == "Write":
            result.add(f"\n{state.sp}{ORANGE}[Write] {inp.get('file_path', '')}{RESET}\n")

        elif name == "Read":
            result.add(f"\n{state.sp}{GREEN}[Read] {inp.get('file_path', '')}{RESET}\n")

        elif name == "Glob":
            result.add(f"\n{state.sp}{PURPLE}[Glob] {inp.get('pattern', '')}{RESET}\n")

        elif name == "Grep":
            pattern = inp.get("pattern", "")
            path = inp.get("path", "")
            if path:
                path = path.split("/")[-1]
                result.add(f'\n{state.sp}{PURPLE}[Grep] "{pattern}" in {path}{RESET}\n')
            else:
                result.add(f'\n{state.sp}{PURPLE}[Grep] "{pattern}"{RESET}\n')

        elif name in ("Edit", "MultiEdit"):
            result.add(f"\n{state.sp}{ORANGE}[{name}] {inp.get('file_path', '')}{RESET}\n")

        elif name == "NotebookEdit":
            result.add(f"\n{state.sp}{ORANGE}[NotebookEdit] {inp.get('notebook_path', '')}{RESET}\n")

        elif name == "Bash":
            result.add(f"\n{state.sp}{PURPLE}[Bash] {inp.get('command', '')}{RESET}\n")

        elif name == "Task":
            prompt = inp.get("prompt", inp.get("description", ""))[:50]
            model = inp.get("model", "sonnet")
            result.add(f'\n{state.sp}{BLUE}[Task] "{prompt}" ({model}){RESET}\n')
            if state.mode == "stream":
                state.increment_depth()
                result.add(f"{state.sp}{DIM}┌───────────────────────────────{RESET}\n")


def _handle_result(data: dict, state: ParserState, result: ParseResult):
    while state.subagent_depth > 0:
        result.add(f"{state.sp}{DIM}└───────────────────────────────{RESET}\n")
        state.decrement_depth()

    if data.get("is_error"):
        result.add(f"\n{RED}[error] {data.get('result', 'unknown error')}{RESET}\n")
    else:
        duration_ms = data.get("duration_ms", 0)
        duration = f"{duration_ms / 1000:.1f}"
        cost = f"{data.get('total_cost_usd', 0):.4f}"
        turns = data.get("num_turns", 0)
        usage = data.get("usage", {})
        input_tokens = sum([
            usage.get("input_tokens", 0),
            usage.get("cache_read_input_tokens", 0),
            usage.get("cache_creation_input_tokens", 0),
        ])
        output_tokens = usage.get("output_tokens", 0)
        result.add(f"\n{DIM}[done] {duration}s, ${cost}, {turns} turns, {input_tokens} in / {output_tokens} out{RESET}\n")
