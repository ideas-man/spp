# spp - Simple Python Prompt

A lightweight, customizable zsh prompt written in Python.

## Install

### Arch Linux (PKGBUILD)

```sh
makepkg -si # -Cfsi
```
and follow the post-isntall instuctions.

## Configuration

Set `SPP_EXPR` in your `.zshrc` to customize the prompt:

```sh
export SPP_EXPR='{?time {status} {time}{nl}}{cyan}{userhost}{reset} {blue}{scwd:3}{reset}{? {yellow} {git}{reset}}{nl}{bold}>{reset} '
```

## Tokens

| Token | Description | Example output |
|---|---|---|
| `{status}` | Exit code number | `0`, `1`, `130` |
| `{exit}` | Exit code name | `SUCCESS`, `SIGSEGV` |
| `{time}` | Elapsed time (human-readable) | `3s`, `2m10s`, `1h5m` |
| `{timer}` | Elapsed time (precise) | `[3.21]` |
| `{git}` | Branch, ahead/behind, dirty state | `main ↑1 ~2 ?1` |
| `{cwd}` | Full working directory | `/home/user/projects/foo` |
| `{hcwd}` | Working directory with `~` | `~/projects/foo` |
| `{scwd}` | Shortened cwd | `~/projects/foo` |
| `{scwd:N}` | Last N path components | `foo` (N=1) |
| `{user}` | Username | `user` |
| `{host}` | Hostname | `host` |
| `{userhost}` | user@host | `user@host` |
| `{eperm}` | Effective permissions on cwd | `rwx` or `r-x` |
| `{operm}` | Octal mode of cwd | `755` |
| `{sep}` | Full-width separator line | `────────...` |
| `{nl}` | Literal newline | |

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
