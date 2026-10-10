#!/usr/bin/env bash
# Regenerate every client from the AsyncAPI document the app serves.
#
#   scripts/sync-clients.sh                       # from the running app
#   scripts/sync-clients.sh path/to/asyncapi.json # from a file (CI)
set -euo pipefail
cd "$(dirname "$0")/.."

SCHEMA="${1:-http://localhost:8000/asyncapi.json}"
case "$SCHEMA" in
  http*) curl -fsS -o /dev/null --max-time 5 "$SCHEMA" \
    || { echo "App not reachable at $SCHEMA. Start it: uv run uvicorn app.main:app" >&2; exit 1; } ;;
  *) SCHEMA="$(cd "$(dirname "$SCHEMA")" && pwd)/$(basename "$SCHEMA")" ;;
esac

echo "==> Python client"
uv run chanx generate-client --schema "$SCHEMA" --output clients/python --no-readme

echo "==> TypeScript client"
(cd web && npx chanx-codegen "$SCHEMA" -o src/generated)
