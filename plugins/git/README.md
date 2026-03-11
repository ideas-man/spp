# git

Git repository context for your prompt.

## Token

| Token | Description | Example |
|---|---|---|
| `{git}` | Branch, ahead/behind, dirty state | `main ↑1 ~2 ?1` |

**Symbols:** `↑` ahead, `↓` behind, `+` staged, `~` modified, `?` untracked

Empty (conditional collapses) when not inside a git repo.

## Aliases

| Alias | Command |
|---|---|
| `gs` | `git status` |
| `gc` | `git commit` |
| `gco` | `git checkout` |
| `gd` | `git diff` |
| `gl` | `git log --oneline` |
| `gp` | `git push` |
| `gpl` | `git pull` |
| `ga` | `git add` |
| `gb` | `git branch` |
| `gst` | `git stash` |

All aliases have zsh completions.
