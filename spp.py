#!/usr/bin/env python3

import os
import re
import argparse
import shutil
import subprocess

COLORS = {
    "red":     "\033[31m",
    "green":   "\033[32m",
    "yellow":  "\033[33m",
    "blue":    "\033[34m",
    "magenta": "\033[35m",
    "cyan":    "\033[36m",
    "white":   "\033[37m",
    "bold":    "\033[1m",
    "dim":     "\033[2m",
    "reset":   "\033[0m",
}

EXIT_CODES = {
    "0": "SUCCESS", "1": "GENERAL", "2": "MISUSE",
    "126": "NOTEXEC", "127": "NOTFOUND", "128": "ABNORMAL", "255": "OUTOFRANGE",
    # Signals 1-5
    "129": "SIGHUP", "130": "SIGINT", "131": "SIGQUIT", "132": "SIGILL", "133": "SIGTRAP",
    # Signals 6-10
    "134": "SIGABRT", "135": "SIGBUS", "136": "SIGFPE", "137": "SIGKILL", "138": "SIGUSR1",
    # Signals 11-15
    "139": "SIGSEGV", "140": "SIGUSR2", "141": "SIGPIPE", "142": "SIGALRM", "143": "SIGTERM",
    # Signals 17-21
    "145": "SIGCHLD", "146": "SIGCONT", "147": "SIGSTOP", "148": "SIGTSTP", "149": "SIGTTIN",
    # Signals 22-26
    "150": "SIGTTOU", "151": "SIGURG", "152": "SIGXCPU", "153": "SIGXFSZ", "154": "SIGVTALRM",
    # Signals 27-31
    "155": "SIGPROF", "156": "SIGWINCH", "157": "SIGPOLL", "158": "SIGPWR", "159": "SIGSYS",
}

_TOKEN_RE = re.compile(r'\{(\w+)(?::(\w+))?\}')
SENTINEL = "\x00"

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

def _get_exit():
    code = os.environ.get("EXIT_STATUS", "0")
    return EXIT_CODES.get(code, "UNKNOWN")

def _get_status():
    return os.environ.get("EXIT_STATUS", "0")

def _human_time():
    s_env = os.environ.get("SECONDS")
    s_start = os.environ.get("SECONDS_START")
    if not s_env or not s_start:
        return ""
    elapsed = int(float(s_env) - float(s_start))
    if elapsed <= 0:
        return ""
    days, rem = divmod(elapsed, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, secs = divmod(rem, 60)
    if days:
        return f"{days}d{hours}h"
    if hours:
        return f"{hours}h{minutes}m"
    if minutes:
        return f"{minutes}m{secs}s"
    return f"{secs}s"

def _exec_timer():
    if os.environ.get("SECONDS") and os.environ.get("SECONDS_START"):
        elapsed = float(os.environ["SECONDS"]) - float(os.environ["SECONDS_START"])
        return f"[{elapsed:.2f}]"
    return ""

def _get_sep():
    cols = shutil.get_terminal_size((80, 24)).columns
    return "─" * cols

def _get_perms():
    cwd = os.getcwd()
    r = "r" if os.access(cwd, os.R_OK) else "-"
    w = "w" if os.access(cwd, os.W_OK) else "-"
    x = "x" if os.access(cwd, os.X_OK) else "-"
    return f"{r}{w}{x}"

def _get_operms():
    return oct(os.stat(os.getcwd()).st_mode)[-3:]

def _short_cwd(depth):
    path = os.getcwd().replace(os.path.expanduser("~"), "~", 1)
    if depth <= 0:
        return path
    parts = [p for p in path.split(os.sep) if p]
    if len(parts) <= depth:
        return path
    return os.sep.join(parts[-depth:])

TOKENS = {
    "status":    lambda: _get_status(),
    "exit":      lambda: _get_exit(),
    "timer":     lambda: _exec_timer(),
    "time":      lambda: _human_time(),
    "git":       lambda: _get_git_info(),
    "cwd":       lambda: os.getcwd(),
    "hcwd":      lambda: os.getcwd().replace(os.path.expanduser("~"), "~", 1),
    "scwd":      lambda: _short_cwd(0),
    "user":      lambda: os.environ.get("USER", ""),
    "host":      lambda: os.uname().nodename,
    "userhost":  lambda: f"{os.environ.get('USER', '')}@{os.uname().nodename}",
    "nl":        lambda: "\n",
    "sep":       lambda: _get_sep(),
    "eperm":     lambda: _get_perms(),
    "operm":     lambda: _get_operms(),
}

def _parse_sections(expr):
    """Parse expr into list of (is_conditional, key_token, content) tuples."""
    sections = []
    i = 0
    while i < len(expr):
        if expr[i:i+2] == '{?':
            # Find closing } that isn't inside a {token}
            depth = 0
            j = i + 2
            while j < len(expr):
                if expr[j] == '{':
                    depth += 1
                elif expr[j] == '}':
                    if depth == 0:
                        break
                    depth -= 1
                j += 1
            raw_content = expr[i+2:j]
            # Check for keyed conditional: {?token content}
            key_match = re.match(r'(\w+) ', raw_content)
            if key_match and key_match.group(1) in TOKENS:
                key_token = key_match.group(1)
                sections.append((True, key_token, raw_content[key_match.end():]))
            else:
                sections.append((True, None, raw_content))
            i = j + 1
        else:
            # Collect literal/token text until next {?
            start = i
            while i < len(expr):
                if expr[i:i+2] == '{?':
                    break
                i += 1
            sections.append((False, None, expr[start:i]))
    return sections

def _resolve_tokens(text, values):
    """Replace {token} and {token:arg} with resolved values."""
    def _replace(m):
        name, arg = m.group(1), m.group(2)
        if name == "scwd" and arg is not None:
            return _short_cwd(int(arg))
        return values.get(name, m.group(0))
    return _TOKEN_RE.sub(_replace, text)

def render(expr, zsh=False):
    expr = expr.encode("raw_unicode_escape").decode("unicode_escape")
    # Build token values including colors
    values = {k: v() for k, v in TOKENS.items()}
    for name, code in COLORS.items():
        values[name] = f"%{{{code}%}}" if zsh else code
    # Track which tokens are empty (colors are decorative, not content)
    color_tokens = set(COLORS.keys())
    empty_tokens = {k for k, v in values.items() if v == ""}
    for k in empty_tokens:
        values[k] = SENTINEL
    # Parse conditional sections, resolve tokens in each, collapse empty conditionals
    parts = []
    for is_cond, key_token, content in _parse_sections(expr):
        resolved = _resolve_tokens(content, values)
        if is_cond:
            if key_token is not None:
                # Keyed conditional: collapse if the named token is empty
                if key_token in empty_tokens:
                    continue
            else:
                # Unkeyed conditional: collapse if every content token is empty
                tokens_here = [(m.group(1)) for m in _TOKEN_RE.finditer(content)]
                content_tokens = [t for t in tokens_here if t not in color_tokens]
                if not any(t not in empty_tokens for t in content_tokens):
                    continue
        parts.append(resolved)
    result = ''.join(parts)
    result = result.replace(SENTINEL, "")
    return result

def parse_args():
    parser = argparse.ArgumentParser(description="Simple Python Prompt")
    parser.add_argument("--expr", "-e", type=str, default="{status}{? {time}}{? {git}}\n>: ",
                        help="Prompt expression with tokens (see README)")
    parser.add_argument("--raw", "-r", action="store_true", help="Strip newlines from output")
    parser.add_argument("--zsh", action="store_true", help="Wrap ANSI codes in %%{...%%} for zsh prompt width")
    return parser.parse_args()

def main():
    args = parse_args()
    output = render(args.expr, zsh=args.zsh)
    if args.raw:
        output = output.replace("\n", "")
    print(output, end="", flush=True)

if __name__ == "__main__":
    main()
