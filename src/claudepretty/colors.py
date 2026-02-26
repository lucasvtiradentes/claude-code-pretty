GREEN = "\033[32m"
ORANGE = "\033[33m"
PURPLE = "\033[35m"
CYAN = "\033[36m"
BLUE = "\033[34m"
YELLOW = "\033[93m"
DIM = "\033[2m"
RED = "\033[31m"
RESET = "\033[0m"


def green(text: str) -> str:
    return f"{GREEN}{text}{RESET}"


def orange(text: str) -> str:
    return f"{ORANGE}{text}{RESET}"


def purple(text: str) -> str:
    return f"{PURPLE}{text}{RESET}"


def cyan(text: str) -> str:
    return f"{CYAN}{text}{RESET}"


def blue(text: str) -> str:
    return f"{BLUE}{text}{RESET}"


def yellow(text: str) -> str:
    return f"{YELLOW}{text}{RESET}"


def dim(text: str) -> str:
    return f"{DIM}{text}{RESET}"


def red(text: str) -> str:
    return f"{RED}{text}{RESET}"
