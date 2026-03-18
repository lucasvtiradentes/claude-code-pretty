import re
from html import escape


class HtmlRenderer:
    def bold(self, text: str) -> str:
        return f'<span class="bold">{escape(text)}</span>'

    def dim(self, text: str) -> str:
        return f'<span class="dim">{escape(text)}</span>'

    def red(self, text: str) -> str:
        return f'<span class="red">{escape(text)}</span>'

    def green(self, text: str) -> str:
        return f'<span class="green">{escape(text)}</span>'

    def orange(self, text: str) -> str:
        return f'<span class="orange">{escape(text)}</span>'

    def purple(self, text: str) -> str:
        return f'<span class="purple">{escape(text)}</span>'

    def cyan(self, text: str) -> str:
        return f'<span class="cyan">{escape(text)}</span>'

    def blue(self, text: str) -> str:
        return f'<span class="blue">{escape(text)}</span>'

    def yellow(self, text: str) -> str:
        return f'<span class="yellow">{escape(text)}</span>'

    def code(self, text: str) -> str:
        return f"<code>{escape(text)}</code>"

    def render_markdown(self, text: str) -> str:
        text = escape(text)
        text = re.sub(r"\*\*(.+?)\*\*", r'<span class="bold">\1</span>', text)
        text = re.sub(r"__(.+?)__", r'<span class="bold">\1</span>', text)
        text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
        return text

    def style_reset(self) -> str:
        return ""

    def style_bold(self) -> str:
        return ""

    def style_code(self) -> str:
        return ""

    def style_bold_code(self) -> str:
        return ""

    def section_open(self) -> str:
        return self.dim("┌" + "─" * 31)

    def section_close(self) -> str:
        return self.dim("└" + "─" * 31)

    def pipe(self) -> str:
        return '<span class="dim">│</span> '
