#!/usr/bin/env python3

import os
import re
import argparse
import importlib.util
from pathlib import Path

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

_TOKEN_RE = re.compile(r'\{(\w+)(?::(\w+))?\}')
SENTINEL = "\x00"

_PLUGIN_DIRS = [
    Path("/usr/share/spp/plugins"),
    Path("~/.config/spp/plugins").expanduser(),
    Path(__file__).resolve().parent / "plugins",
]

def _load_plugins():
    plugins = os.environ.get("SPP_PLUGINS", "").split()
    for name in plugins:
        for base in _PLUGIN_DIRS:
            tokens_path = base / name / "tokens.py"
            if tokens_path.is_file():
                try:
                    spec = importlib.util.spec_from_file_location(
                        f"spp_plugin_{name}", tokens_path)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    mod.register(TOKENS)
                except Exception:
                    pass
                break

TOKENS = {}

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

def _resolve_tokens(text, values, tokens):
    """Replace {token} and {token:arg} with resolved values."""
    def _replace(m):
        name, arg = m.group(1), m.group(2)
        if arg is not None:
            fn = tokens.get(name)
            if fn:
                try:
                    return fn(arg)
                except TypeError:
                    pass
        return values.get(name, m.group(0))
    return _TOKEN_RE.sub(_replace, text)

def render(expr, zsh=False):
    expr = expr.encode("raw_unicode_escape").decode("unicode_escape")
    _load_plugins()
    # Lazy evaluation: only call lambdas for tokens referenced in the expression
    referenced = set(m.group(1) for m in _TOKEN_RE.finditer(expr))
    values = {k: v() for k, v in TOKENS.items() if k in referenced}
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
        resolved = _resolve_tokens(content, values, TOKENS)
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
    parser.add_argument("--expr", "-e", type=str, default=">: ",
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
