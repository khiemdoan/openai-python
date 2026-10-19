from __future__ import annotations

import importlib.util
from typing import Any, cast

import httpx2

from openai import DefaultHttpx2Client, DefaultAsyncHttpx2Client


def _pool_http2(client: httpx2.Client | httpx2.AsyncClient) -> bool:
    transport = cast(Any, client._transport)
    return cast(bool, transport._pool._http2)


def test_httpx2_http2_extra_installs_h2() -> None:
    assert importlib.util.find_spec("h2") is not None

    with httpx2.Client(http2=True) as client:
        assert _pool_http2(client) is True


def test_default_helpers_preserve_the_http2_transport_option() -> None:
    sync_client = DefaultHttpx2Client(http2=True)
    try:
        assert _pool_http2(sync_client) is True
    finally:
        sync_client.close()

    default_sync_client = DefaultHttpx2Client()
    try:
        assert _pool_http2(default_sync_client) is False
    finally:
        default_sync_client.close()


async def test_default_async_helpers_preserve_the_http2_transport_option() -> None:
    async_client = DefaultAsyncHttpx2Client(http2=True)
    try:
        assert _pool_http2(async_client) is True
    finally:
        await async_client.aclose()

    default_async_client = DefaultAsyncHttpx2Client()
    try:
        assert _pool_http2(default_async_client) is False
    finally:
        await default_async_client.aclose()
