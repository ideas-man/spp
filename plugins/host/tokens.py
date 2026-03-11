import os


def register(tokens):
    tokens["user"] = lambda: os.environ.get("USER", "")
    tokens["host"] = lambda: os.uname().nodename
    tokens["userhost"] = lambda: f"{os.environ.get('USER', '')}@{os.uname().nodename}"
