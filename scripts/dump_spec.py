"""Print the AsyncAPI document for the app, without starting a server.

    uv run python scripts/dump_spec.py > asyncapi.json
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from chanx.fast_channels.views import generate_asyncapi_schema  # noqa: E402
from starlette.requests import Request  # noqa: E402

from app.main import app, asyncapi_config  # noqa: E402

# The generator reads the host from a request, so give it a fixed one.
request = Request(
    {
        "type": "http",
        "method": "GET",
        "scheme": "http",
        "path": "/",
        "query_string": b"",
        "headers": [(b"host", b"localhost:8000")],
        "server": ("localhost", 8000),
    }
)

spec = generate_asyncapi_schema(request, app, asyncapi_config)
print(json.dumps(spec, indent=2, sort_keys=True))
