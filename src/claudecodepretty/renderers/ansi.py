import re

BOLD = "\033[1m"
INVERSE = "\033[7m"
GREEN = "\033[32m"
ORANGE = "\033[33m"
PURPLE = "\033[35m"
BLUE = "\033[34m"
YELLOW = "\033[93m"
DIM = "\033[90m"
RED = "\033[31m"
RESET = "\033[0m"


class AnsiRenderer:
    def bold(self, text: str) -> str:
        return f"{BOLD}{text}{RESET}"

    def dim(self, text: str) -> str:
        return f"{DIM}{text}{RESET}"

    def red(self, text: str) -> str:
        return f"{RED}{text}{RESET}"

    def green(self, text: str) -> str:
        return f"{GREEN}{text}{RESET}"

    def orange(self, text: str) -> str:
        return f"{ORANGE}{text}{RESET}"

    def purple(self, text: str) -> str:
        return f"{PURPLE}{text}{RESET}"

    def blue(self, text: str) -> str:
        return f"{BLUE}{text}{RESET}"

    def yellow(self, text: str) -> str:
        return f"{YELLOW}{text}{RESET}"

    def render_markdown(self, text: str) -> str:
        text = re.sub(r"\*\*(.+?)\*\*", rf"{BOLD}\1{RESET}", text)
        text = re.sub(r"__(.+?)__", rf"{BOLD}\1{RESET}", text)
        text = re.sub(r"`([^`]+)`", rf"{INVERSE}\1{RESET}", text)
        return text

    def style_reset(self) -> str:
        return RESET

    def style_bold(self) -> str:
        return BOLD

    def style_code(self) -> str:
        return INVERSE

    def style_bold_code(self) -> str:
        return BOLD + INVERSE

    def section_open(self) -> str:
        return self.dim("┌" + "─" * 31)

    def section_close(self) -> str:
        return self.dim("└" + "─" * 31)

    def pipe(self) -> str:
        return f"{DIM}│{RESET} "
