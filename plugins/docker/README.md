# docker

Docker context awareness for your prompt.

## Token

| Token | Description | Example |
|---|---|---|
| `{docker}` | Active Docker context name | `staging` |

Detection (fast path first):
1. `$DOCKER_CONTEXT` env var
2. `~/.docker/config.json` → `currentContext`
3. `docker context show` subprocess (2s timeout)

Empty when context is `"default"` or undetectable.

## Aliases

| Alias | Command |
|---|---|
| `dps` | `docker ps` |
| `dpsa` | `docker ps -a` |
| `dex` | `docker exec -it` |
| `dlog` | `docker logs -f` |
| `dimg` | `docker images` |
| `drm` | `docker rm` |
| `drmi` | `docker rmi` |
| `dcu` | `docker compose up` |
| `dcd` | `docker compose down` |
| `dcr` | `docker compose restart` |
| `dcl` | `docker compose logs -f` |
| `dcb` | `docker compose build` |

All aliases have zsh completions.
