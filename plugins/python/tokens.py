import os
from pathlib import Path


def _get_venv():
    venv = os.environ.get("VIRTUAL_ENV")
    if venv:
        return Path(venv).name
    conda = os.environ.get("CONDA_DEFAULT_ENV")
    if conda and conda != "base":
        return conda
    return ""


def register(tokens):
    tokens["venv"] = _get_venv
