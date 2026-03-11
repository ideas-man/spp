import os
import json
import subprocess
from pathlib import Path


def _get_docker_context():
    # Fast: env var (set by `docker context use` or manually)
    ctx = os.environ.get("DOCKER_CONTEXT")
    if not ctx:
        # Medium: read config file
        config = Path.home() / ".docker" / "config.json"
        if config.is_file():
            try:
                ctx = json.loads(config.read_text()).get("currentContext")
            except (json.JSONDecodeError, OSError):
                pass
    if not ctx:
        # Slow: subprocess fallback
        try:
            r = subprocess.run(
                ["docker", "context", "show"],
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                text=True, timeout=2,
            )
            if r.returncode == 0:
                ctx = r.stdout.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
    if not ctx or ctx == "default":
        return ""
    return ctx


def register(tokens):
    tokens["docker"] = _get_docker_context
