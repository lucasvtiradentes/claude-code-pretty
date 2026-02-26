from claudecodepretty.colors import DIM, RESET
from claudecodepretty.constants import INDENT
from claudecodepretty.handlers.base import ParseResult, ParserState


def handle_system(data: dict, state: ParserState, result: ParseResult):
    if data.get("subtype") == "init":
        session_id = data.get("session_id", "")
        cwd = data.get("cwd", "").replace("/", "-").replace("_", "-")
        model = data.get("model", "")
        model_name = model.split("-")[1] if "-" in model else model

        result.add(f"{DIM}[session]\n")
        result.add(f"{INDENT}id:    {session_id}\n")
        result.add(f"{INDENT}path:  ~/.claude/projects/{cwd}/{session_id}.jsonl\n")
        result.add(f"{INDENT}model: {model_name}{RESET}\n\n")
