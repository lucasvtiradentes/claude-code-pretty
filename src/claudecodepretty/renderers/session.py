from html import escape

from claudecodepretty.handlers.base import ParserState
from claudecodepretty.parser import parse_json_line
from claudecodepretty.renderers.html import HtmlRenderer
from claudecodepretty.renderers.template import SESSION_HTML_TEMPLATE


def parse_session_to_html(file_path: str) -> str:
    renderer = HtmlRenderer()
    state = ParserState(mode="replay", renderer=renderer)
    fragments = []

    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                result = parse_json_line(line, state)
                output = result.get_output()
                if output:
                    fragments.append(output)

    content = "".join(fragments)

    return SESSION_HTML_TEMPLATE.format(
        title=f"Session - {escape(file_path.split('/')[-1])}",
        meta=escape(file_path),
        content=content,
    )
