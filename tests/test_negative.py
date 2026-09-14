from __future__ import annotations

import httpx
import pytest
import respx

from src.gitlab_client import GitLab, assert_status

pytestmark = pytest.mark.unit


@respx.mock
async def test_unauthorized_without_token(gitlab_mock: GitLab) -> None:
    route = respx.get(
        f"{gitlab_mock.base_url}/api/v4/projects/{gitlab_mock.project_id}/issues"
    ).mock(
        return_value=httpx.Response(401, json={"message": "401 Unauthorized"})
    )

    async with GitLab(
        base_url=gitlab_mock.base_url,
        project_id=gitlab_mock.project_id,
        token="",
    ) as client:
        response = await client.get_issues()

    assert_status(response, 401)
    assert response.json()["message"] == "401 Unauthorized"
    assert route.called


@respx.mock
async def test_issue_not_found(gitlab_mock: GitLab) -> None:
    missing_iid = 999999
    route = respx.get(
        f"{gitlab_mock.base_url}/api/v4/projects/{gitlab_mock.project_id}/issues/{missing_iid}"
    ).mock(
        return_value=httpx.Response(404, json={"message": "404 Not found"})
    )

    response = await gitlab_mock.get_issue_by_id(missing_iid)

    assert_status(response, 404)
    assert response.json()["message"] == "404 Not found"
    assert route.called
