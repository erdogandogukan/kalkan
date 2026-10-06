import json

import httpx
from fastapi.testclient import TestClient

from kalkan.proxy import create_app


def _completion(content: str) -> dict:
    return {
        "id": "chatcmpl-test",
        "object": "chat.completion",
        "model": "fake-model",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": content},
                "finish_reason": "stop",
            }
        ],
    }


def _client(reply: str = "ok") -> tuple[TestClient, list[dict]]:
    """A proxy client whose upstream is fake; returns the client and the requests upstream saw."""
    seen: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(json.loads(request.content))
        return httpx.Response(200, json=_completion(reply))

    upstream = httpx.AsyncClient(
        base_url="http://upstream.test/v1", transport=httpx.MockTransport(handler)
    )
    return TestClient(create_app(upstream=upstream)), seen


def _post(client: TestClient, messages: list[dict], **extra) -> httpx.Response:
    return client.post(
        "/v1/chat/completions", json={"model": "fake-model", "messages": messages, **extra}
    )


def test_p1_upstream_gets_masked_content() -> None:
    client, seen = _client()
    _post(client, [{"role": "user", "content": "TC'm 10000000146"}])

    sent = json.dumps(seen[0], ensure_ascii=False)
    assert "10000000146" not in sent
    assert "[TCKN_1]" in sent


def test_p2_reply_labels_are_restored() -> None:
    client, _ = _client(reply="[TCKN_1] numaralı...")
    response = _post(client, [{"role": "user", "content": "TC'm 10000000146"}])

    assert response.status_code == 200
    assert response.json()["choices"][0]["message"]["content"] == "10000000146 numaralı..."


def test_p3_one_mapping_across_messages() -> None:
    client, seen = _client(reply="[TCKN_1] ve [TCKN_2]")
    response = _post(
        client,
        [
            {"role": "system", "content": "Kullanıcı: 10000000146"},
            {"role": "user", "content": "Eşim: 34567891238"},
        ],
    )

    sent = seen[0]["messages"]
    assert sent[0]["content"] == "Kullanıcı: [TCKN_1]"
    assert sent[1]["content"] == "Eşim: [TCKN_2]"
    assert response.json()["choices"][0]["message"]["content"] == "10000000146 ve 34567891238"


def test_p4_stream_is_rejected_without_calling_upstream() -> None:
    client, seen = _client()
    response = _post(client, [{"role": "user", "content": "TC'm 10000000146"}], stream=True)

    assert response.status_code == 400
    assert seen == []


def test_p5_unreachable_upstream_returns_502() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("connection refused", request=request)

    upstream = httpx.AsyncClient(
        base_url="http://upstream.test/v1", transport=httpx.MockTransport(handler)
    )
    client = TestClient(create_app(upstream=upstream))
    response = _post(client, [{"role": "user", "content": "Merhaba"}])

    assert response.status_code == 502
