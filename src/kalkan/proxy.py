"""OpenAI-compatible proxy: masks TCKNs before the LLM sees them and restores them in the reply.

Run with: python -m kalkan.proxy  (listens on 127.0.0.1:8000 only)
"""

import logging
import os
from typing import Any

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from kalkan.pii.mask import mask_tckns, unmask

logger = logging.getLogger("kalkan.proxy")

DEFAULT_UPSTREAM_URL = "http://localhost:11434/v1"


def _error(status: int, message: str) -> JSONResponse:
    return JSONResponse(status_code=status, content={"error": {"message": message}})


def _mask_messages(messages: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, str]]:
    """Mask every message (any role) with one shared label map."""
    mapping: dict[str, str] = {}
    masked: list[dict[str, Any]] = []
    for message in messages:
        message = dict(message)
        content = message.get("content")
        if isinstance(content, str):
            message["content"], mapping = mask_tckns(content, mapping)
        elif isinstance(content, list):
            parts = []
            for part in content:
                if isinstance(part, dict) and isinstance(part.get("text"), str):
                    part = dict(part)
                    part["text"], mapping = mask_tckns(part["text"], mapping)
                parts.append(part)
            message["content"] = parts
        masked.append(message)
    return masked, mapping


def create_app(upstream: httpx.AsyncClient | None = None) -> FastAPI:
    """Build the proxy app. upstream is the client for the LLM server (injected in tests)."""
    if upstream is None:
        upstream = httpx.AsyncClient(
            base_url=os.environ.get("KALKAN_UPSTREAM_URL", DEFAULT_UPSTREAM_URL), timeout=120
        )

    app = FastAPI(title="Kalkan")

    @app.post("/v1/chat/completions")
    async def chat_completions(request: Request) -> JSONResponse:
        try:
            body = await request.json()
        except ValueError:
            return _error(400, "request body must be JSON")
        if not isinstance(body, dict) or not isinstance(body.get("messages"), list):
            return _error(400, "'messages' must be a list")
        # Streaming would need unmasking across chunks; refuse instead of passing anything through.
        if body.get("stream"):
            return _error(400, "streaming henüz desteklenmiyor")

        messages, mapping = _mask_messages(body["messages"])
        body = {**body, "messages": messages}
        # Only masked content is ever logged.
        logger.info("to LLM: %s", messages)

        try:
            response = await upstream.post("chat/completions", json=body)
        except httpx.RequestError as exc:
            logger.warning("upstream unreachable: %s", type(exc).__name__)
            return _error(502, "LLM server is unreachable")

        try:
            data = response.json()
        except ValueError:
            return _error(502, "LLM server returned a non-JSON response")
        if response.is_error:
            return JSONResponse(status_code=response.status_code, content=data)

        for choice in data.get("choices") or []:
            message = choice.get("message") or {}
            if isinstance(message.get("content"), str):
                message["content"] = unmask(message["content"], mapping)
        return JSONResponse(content=data)

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="127.0.0.1", port=8000)
