import shutil


def _get_sep():
    cols = shutil.get_terminal_size((80, 24)).columns
    return "─" * cols


def register(tokens):
    tokens["nl"] = lambda: "\n"
    tokens["sep"] = lambda: _get_sep()
