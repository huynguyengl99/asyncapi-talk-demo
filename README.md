# asyncapi-talk-demo

Demo for the talk "Keeping WebSocket APIs honest with AsyncAPI: a code-first approach in Python" at AsyncAPI Conference: Online Edition 2026.

A small FastAPI room chat built with [chanx](https://github.com/huynguyengl99/chanx). The typed handlers in `app/` are the contract. Everything else is generated from them:

| Path | What | Made by |
| --- | --- | --- |
| `app/messages.py`, `app/consumer.py` | Pydantic messages and typed handlers | you |
| `asyncapi.json` | AsyncAPI 3.0 document, committed | `scripts/dump_spec.py` |
| `clients/python/` | Typed Python client | `chanx generate-client` |
| `web/src/generated/` | Typed TypeScript client | `@chanx-js/codegen` |
| `.github/workflows/contract.yml` | Contract checks on every pull request | CI |

## Run it

```bash
uv sync
uv run uvicorn app.main:app --reload
```

Open http://localhost:8000/asyncapi for the docs page, or http://localhost:8000/asyncapi.json for the raw document. The chat endpoint is `ws://localhost:8000/ws/room/{room_name}`.

## Regenerate after changing a handler

```bash
uv run python scripts/dump_spec.py > asyncapi.json
uv run chanx generate-client --schema asyncapi.json --output clients/python
npm install --prefix web
npm run --prefix web gen
npm run --prefix web typecheck
```

## What CI checks

1. The committed `asyncapi.json` matches the code.
2. The document is valid AsyncAPI (`asyncapi validate`).
3. No breaking change against the base branch (`asyncapi diff --type=breaking`, checked with `jq`, because the command exits 0 even when it finds breaking changes).
4. The frontend still compiles against the regenerated TypeScript client.

`asyncapi diff` reports a removed channel as breaking, but a renamed payload field as "unclassified". Step 4 is the check that catches payload renames.
