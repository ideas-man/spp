# fs

Working directory and permissions tokens.

## Tokens

| Token | Description | Example |
|---|---|---|
| `{cwd}` | Full working directory | `/home/user/projects/foo` |
| `{hcwd}` | Working directory with `~` | `~/projects/foo` |
| `{scwd}` | Shortened cwd | `~/projects/foo` |
| `{scwd:N}` | Last N path components | `foo` (N=1) |
| `{eperm}` | Effective permissions on cwd | `rwx` or `r-x` |
| `{operm}` | Octal mode of cwd | `755` |
