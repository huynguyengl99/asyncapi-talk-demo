# asyncapi-talk-demo

Demo for the talk "Keeping WebSocket APIs honest with AsyncAPI: a code-first approach in Python" at AsyncAPI Conference: Online Edition 2026.

A small FastAPI room chat built with [chanx](https://github.com/huynguyengl99/chanx). The typed handlers in `app/` are the contract. The app serves its AsyncAPI document, and the clients are generated from it:

| Path | What | Made by |
| --- | --- | --- |
| `app/messages.py`, `app/consumer.py` | Pydantic messages and typed handlers | you |
| `/asyncapi.json` | AsyncAPI 3.0 document, served by the app (not committed) | chanx, at runtime |
| `clients/python/` | Typed Python client, committed | `scripts/sync-clients.sh` |
| `web/src/generated/` | Typed TypeScript client, committed | `scripts/sync-clients.sh` |
| `.github/workflows/contract.yml` | Contract checks on every pull request | CI |

The generated clients are committed on purpose: when a handler changes, the pull request shows exactly how each client changes.

## Run it

```bash
uv sync
npm install --prefix web
uv run uvicorn app.main:app --reload
```

Open http://localhost:8000/asyncapi for the docs page, or http://localhost:8000/asyncapi.json for the raw document. The chat endpoint is `ws://localhost:8000/ws/room/{room_name}`.

## After changing a handler

With the app running:

```bash
scripts/sync-clients.sh
npm run --prefix web typecheck
```

## What CI checks

CI has no running app, so `scripts/dump_spec.py` builds the document straight from the code.

1. The committed clients match the code (regenerate, then `git diff --exit-code`).
2. The document is valid AsyncAPI (`asyncapi validate`).
3. The frontend still compiles against the regenerated TypeScript client.

A contract change shows up in review as a diff of the generated clients. A breaking change fails step 3.

## The two demo changes

Each one is a tag on top of `main`:

| Tag | Change | What CI says |
| --- | --- | --- |
| `demo-rename-field` | Payload field `message` renamed to `text`, clients regenerated and committed | Steps 1 and 2 pass. Step 3 fails: the frontend still reads `payload.message`. |
| `demo-remove-channel` | Room chat endpoint removed (the health channel stays) | Steps 1 and 2 pass. Step 3 fails: the frontend imports `roomChat`, which no longer exists. |

```bash
git checkout demo-rename-field
npm run --prefix web typecheck

git checkout main
```
