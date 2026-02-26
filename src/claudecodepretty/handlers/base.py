from dataclasses import dataclass, field

from claudecodepretty.colors import BOLD, DIM, RESET


@dataclass
class ParserState:
    mode: str = "stream"
    current_tool: str = ""
    subagent_depth: int = 0
    sp: str = ""
    in_bold: bool = False
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

    def render_text(self, text: str) -> str:
        out = []
        i = 0
        buf = self.pending_char + text
        self.pending_char = ""

        while i < len(buf):
            if buf[i] == "*":
                if i + 1 < len(buf):
                    if buf[i + 1] == "*":
                        if self.in_bold:
                            out.append(RESET)
                        else:
                            out.append(BOLD)
                        self.in_bold = not self.in_bold
                        i += 2
                        continue
                    else:
                        out.append(buf[i])
                        i += 1
                else:
                    self.pending_char = "*"
                    break
            else:
                out.append(buf[i])
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
