import subprocess


def _run_git(*args):
    try:
        r = subprocess.run(
            ["git"] + list(args),
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            text=True, timeout=2,
        )
        if r.returncode == 0:
            return r.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def _get_git_info():
    if _run_git("rev-parse", "--is-inside-work-tree") is None:
        return ""

    # Branch or detached HEAD
    branch = _run_git("symbolic-ref", "--short", "HEAD")
    if branch is None:
        branch = _run_git("rev-parse", "--short", "HEAD") or "?"

    # Ahead/behind
    ahead = behind = 0
    ab = _run_git("rev-list", "--count", "--left-right", "HEAD...@{upstream}")
    if ab:
        parts = ab.split()
        if len(parts) == 2:
            ahead, behind = int(parts[0]), int(parts[1])

    # Porcelain status
    porcelain = _run_git("status", "--porcelain")
    staged = modified = untracked = 0
    if porcelain:
        for line in porcelain.splitlines():
            if len(line) < 2:
                continue
            x, y = line[0], line[1]
            if x == "?":
                untracked += 1
            else:
                if x in "MADRC":
                    staged += 1
                if y in "MD":
                    modified += 1

    parts = [branch]
    if ahead:
        parts.append(f"↑{ahead}")
    if behind:
        parts.append(f"↓{behind}")
    if staged:
        parts.append(f"+{staged}")
    if modified:
        parts.append(f"~{modified}")
    if untracked:
        parts.append(f"?{untracked}")
    return " ".join(parts)


def register(tokens):
    tokens["git"] = lambda: _get_git_info()
