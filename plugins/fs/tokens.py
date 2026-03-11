import os
from pathlib import Path


def _short_cwd(depth=0):
    cwd = Path.cwd()
    try:
        path = "~" / cwd.relative_to(Path.home())
    except ValueError:
        path = cwd
    path = str(path)
    if depth <= 0:
        return path
    parts = [p for p in path.split("/") if p]
    if len(parts) <= depth:
        return path
    return "/".join(parts[-depth:])


def _get_perms():
    cwd = Path.cwd()
    r = "r" if os.access(cwd, os.R_OK) else "-"
    w = "w" if os.access(cwd, os.W_OK) else "-"
    x = "x" if os.access(cwd, os.X_OK) else "-"
    return f"{r}{w}{x}"


def _get_operms():
    return oct(Path.cwd().stat().st_mode)[-3:]


def register(tokens):
    tokens["cwd"] = lambda: str(Path.cwd())
    tokens["hcwd"] = lambda: str(Path("~") / Path.cwd().relative_to(Path.home())) if Path.cwd().is_relative_to(Path.home()) else str(Path.cwd())
    tokens["scwd"] = lambda arg=None: _short_cwd(int(arg) if arg else 0)
    tokens["eperm"] = lambda: _get_perms()
    tokens["operm"] = lambda: _get_operms()
