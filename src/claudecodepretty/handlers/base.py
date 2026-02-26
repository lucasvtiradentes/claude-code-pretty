from dataclasses import dataclass, field

from claudecodepretty.colors import BOLD, DIM, INVERSE, RESET


@dataclass
class ParserState:
    mode: str = "stream"
    current_tool: str = ""
    subagent_depth: int = 0
    sp: str = ""
    in_bold: bool = False
    in_code: bool = False
    pending_char: str = ""

    def update_sp(self):
        self.sp = "".join(f"{DIM}│{RESET} " for _ in range(self.subagent_depth))

    def increment_depth(self):
        self.subagent_depth += 1
        self.update_sp()

    def decrement_depth(self):
        if self.subagent_depth > 0:
            self.subagent_depth -= 1
            self.update_sp()

    def _get_style(self) -> str:
        if self.in_bold and self.in_code:
            return BOLD + INVERSE
        if self.in_bold:
            return BOLD
        if self.in_code:
            return INVERSE
        return ""

    def render_text(self, text: str) -> str:
        out = []
        i = 0
        buf = self.pending_char + text
        self.pending_char = ""

        while i < len(buf):
            ch = buf[i]
            if ch == "*" and not self.in_code:
                if i + 1 < len(buf):
                    if buf[i + 1] == "*":
                        self.in_bold = not self.in_bold
                        out.append(RESET + self._get_style())
                        i += 2
                        continue
                    else:
                        out.append(ch)
                        i += 1
                else:
                    self.pending_char = "*"
                    break
            elif ch == "`":
                self.in_code = not self.in_code
                out.append(RESET + self._get_style())
                i += 1
            else:
                out.append(ch)
                i += 1

        return "".join(out)


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
