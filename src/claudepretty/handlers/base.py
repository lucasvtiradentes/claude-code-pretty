from dataclasses import dataclass, field

from claudepretty.colors import DIM, RESET


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
