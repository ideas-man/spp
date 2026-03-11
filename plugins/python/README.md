# python

Python virtual environment context for your prompt.

## Token

| Token | Description | Example |
|---|---|---|
| `{venv}` | Active virtualenv name | `myproject` |

Reads from `$VIRTUAL_ENV` or `$CONDA_DEFAULT_ENV`. Empty when no environment is active.

## Aliases

| Alias | Command |
|---|---|
| `va` | `source .venv/bin/activate` |
| `vd` | `deactivate` |
| `vc` | `python -m venv .venv` |
| `pipi` | `pip install` |
| `pipu` | `pip uninstall` |
| `pipr` | `pip install -r requirements.txt` |
| `pipf` | `pip freeze` |

Pip aliases have zsh completions.
