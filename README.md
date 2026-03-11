# spp - Simple Python Prompt

A lightweight, customizable zsh prompt written in Python.

## Install

### Arch Linux (PKGBUILD)

```sh
makepkg -si # -Cfsi
```
and follow the post-isntall instuctions.

## Configuration

Set `SPP_PLUGINS` and `SPP_EXPR` in your `.zshrc` to customize the prompt:

```sh
export SPP_PLUGINS='shell fs host format git'
export SPP_EXPR='{?time {status} {time}{nl}}{cyan}{userhost}{reset} {blue}{scwd:3}{reset}{? {yellow} {git}{reset}}{nl}{bold}>{reset} '
```

## Plugins

spp supports an oh-my-zsh-style plugin system. Plugins can provide tokens, shell aliases, and zsh completions.

Tokens should answer "what will my next command target?" - not "what is the state of the world?" They are navigational context (which branch, which venv, which docker context), not dashboards. Keep them fast, safe to fail, and composable through conditionals.

### Activation

Set `SPP_PLUGINS` in your `.zshrc` (space-separated list):

```sh
export SPP_PLUGINS='shell fs host format git'
```

No plugins are loaded by default. If `SPP_PLUGINS` is unset, spp renders a bare `>: ` prompt.

### Plugin structure

```
plugins/<name>/
├── tokens.py        # def register(tokens): ...
├── aliases.zsh      # shell aliases
└── completions.zsh  # zsh compdef entries
```

All three files are optional. `tokens.py` is loaded at render time by `spp.py`; `aliases.zsh` and `completions.zsh` are sourced at shell startup by `spp.zsh`.

### Discovery

Plugin directories are searched in order (first match wins):

1. `/usr/share/spp/plugins/` (system - shipped with package)
2. `~/.config/spp/plugins/` (user)
3. `<spp-script-dir>/plugins/` (development)

### Writing a plugin

Create a directory under `~/.config/spp/plugins/<name>/` with a `tokens.py`:

```python
def register(tokens):
    tokens["mytoken"] = lambda: "hello"
```

Then add `<name>` to `SPP_PLUGINS`.

## Tokens

Tokens are provided by plugins - see each plugin's README for available tokens and examples.

### Colors

`{red}` `{green}` `{yellow}` `{blue}` `{magenta}` `{cyan}` `{white}` `{bold}` `{dim}` `{reset}`

## Conditionals

### Unkeyed: `{? ...}`

Collapses the block when **all** content tokens inside are empty. Colors are ignored when checking.

```sh
# Git info only appears when inside a git repo
'{? {yellow}{git}{reset}}'
```

### Keyed: `{?token ...}`

Collapses the block when the **named** token is empty, regardless of other tokens.

```sh
# Only show status + time line when {time} is non-empty
'{?time {status} {time}{nl}}'
```

This is useful when a block contains tokens that are never empty (like `{status}`), but should still be hidden based on a specific token.

## Examples

### Minimal

```sh
export SPP_EXPR='{status} > '
```
```
0 >
```

### Single-line with git

```sh
export SPP_EXPR='{status}{? {dim}{time}{reset}}{? {yellow} {git}{reset}} {blue}{scwd:2}{reset} > '
```
```
0 3s main ~1 projects/foo >
1 projects/foo >
```

### Two-line with status bar

```sh
export SPP_EXPR='{?time {status} {time}{nl}}{cyan}{userhost}{reset} {blue}{scwd:3}{reset}{? {yellow} {git}{reset}}{nl}{bold}>{reset} '
```

After a timed command:
```
0 3s
user@host projects/foo main
>
```

First prompt or instant commands (no timing):
```
user@host projects/foo main
>
```

### Powerline-style

```sh
export SPP_EXPR='{bold}{status}{reset}{? {dim} {time}{reset}} {blue}{scwd:3}{reset}{? {yellow} ({git}){reset}{nl}}{bold}${reset} '
```
```
0 2m10s ~/src/myapp (main ↑1 ~2)
$
```

### Verbose with permissions

```sh
export SPP_EXPR='{exit}{? {time}} [{eperm}] {hcwd}{? {git} [{git}]}{nl}> '
```
```
SIGSEGV 5s [r-x] ~/projects/foo [main +1 ~3 ?2]
>
```

### Three-line dashboard

```sh
export SPP_EXPR='{?time {dim}[{time}] [{status}] [{exit}]{nl}{sep}{reset}{nl}}{white}{scwd:4} [{eperm}/{operm}]{reset}{? [{git}]}{nl}{magenta}{bold}{userhost} >:{reset} '
```

After a timed command in a git repo:
```
[3s] [0] [SUCCESS]
────────────────────────────────────────
~/src/projects/myapp [rwx/755] [main ↑1 ~2]
user@host >:
```

First prompt or instant command (no timing):
```
~/src/projects/myapp [rwx/755] [main ↑1 ~2]
user@host >:
```

Outside a git repo:
```
/etc [r-x/755]
user@host >:
```
