from __future__ import annotations

import os
from typing import Any

import httpx


def env_or_default(name: str, default: str) -> str:
    "Пустая переменная окружения не должна подменять значение по умолчанию."
    value = os.environ.get(name, "").strip()
    return value or default


def assert_status(response: httpx.Response, expected: int) -> None:
    assert response.status_code == expected, (
        f"expected {expected}, got {response.status_code}: {response.text[:500]}"
    )


class GitLab:
    def __init__(
        self,
        base_url: str | None = None,
        project_id: str | None = None,
        token: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.project_id = project_id
        self.token = token
        headers: dict[str, str] = {}
        
        if token:
            headers["PRIVATE-TOKEN"] = token

        self._client = httpx.AsyncClient(self.base_url, headers, timeout)

    def _url(self, suffix: str) -> str:
        return f"/api/v4/projects/{self.project_id}{suffix}"

    async def get_issues(self, params: dict[str, Any] | None = None) -> httpx.Response:
        return await self._client.get(self._url("/issues"), params=params)

    async def get_issue_by_id(
        self,
        iid: int,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:
        return await self._client.get(self._url(f"/issues/{iid}"), params=params)

    async def get_mrs(self, params: dict[str, Any] | None = None) -> httpx.Response:
        return await self._client.get(self._url("/merge_requests"), params=params)

    async def get_mr_by_id(
        self,
        iid: int,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:
        return await self._client.get(
            self._url(f"/merge_requests/{iid}"),
            params=params,
        )

    async def aclose(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> GitLab:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.aclose()
