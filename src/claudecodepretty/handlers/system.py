from claudecodepretty.constants import INDENT
from claudecodepretty.handlers.base import ParseResult, ParserState


def handle_system(data: dict, state: ParserState, result: ParseResult):
    r = state.renderer

    if data.get("subtype") == "init":
        session_id = data.get("session_id", "")
        cwd = data.get("cwd", "").replace("/", "-").replace("_", "-")
        model = data.get("model", "")
        model_name = model.split("-")[1] if "-" in model else model

        lines = (
            f"[session]\n"
            f"{INDENT}id:    {session_id}\n"
            f"{INDENT}path:  ~/.claude/projects/{cwd}/{session_id}.jsonl\n"
            f"{INDENT}model: {model_name}"
        )
        result.add(f"{r.dim(lines)}\n\n")
