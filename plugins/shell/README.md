# shell

Exit status and timing tokens.

## Tokens

| Token | Description | Example |
|---|---|---|
| `{status}` | Exit code number | `0`, `1`, `130` |
| `{exit}` | Exit code name | `SUCCESS`, `SIGSEGV` |
| `{time}` | Elapsed time (human-readable) | `3s`, `2m10s`, `1h5m` |
| `{timer}` | Elapsed time (precise) | `[3.21]` |

`{time}` and `{timer}` are empty (conditional collapses) when no timing data is available.
