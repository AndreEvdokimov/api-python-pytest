from __future__ import annotations

import httpx
import pytest
import respx

from src.gitlab_client import GitLab, assert_status

pytestmark = pytest.mark.unit


def _issues_url(gitlab: GitLab, iid: int | None = None) -> str:
    path = f"{gitlab.base_url}/api/v4/projects/{gitlab.project_id}/issues"
    return f"{path}/{iid}" if iid is not None else path


def _mrs_url(gitlab: GitLab, iid: int | None = None) -> str:
    path = f"{gitlab.base_url}/api/v4/projects/{gitlab.project_id}/merge_requests"
    return f"{path}/{iid}" if iid is not None else path


@pytest.mark.smoke
@respx.mock
async def test_get_issues(gitlab_mock: GitLab, issues_payload: list[dict]) -> None:
    route = respx.get(_issues_url(gitlab_mock)).mock(
        return_value=httpx.Response(200, json=issues_payload)
    )

    response = await gitlab_mock.get_issues()
    body = response.json()

    assert_status(response, 200)
    assert len(body) == len(issues_payload)
    assert body[0]["iid"] == issues_payload[0]["iid"]
    assert body[0]["title"] == issues_payload[0]["title"]
    assert route.called


@respx.mock
@pytest.mark.parametrize("requesting_issue_iid", [333, 444, 555])
async def test_get_issue_by_id(
    gitlab_mock: GitLab,
    issue_payload: dict,
    requesting_issue_iid: int,
) -> None:
    payload = {**issue_payload, "iid": requesting_issue_iid}
    route = respx.get(_issues_url(gitlab_mock, requesting_issue_iid)).mock(
        return_value=httpx.Response(200, json=payload)
    )

    response = await gitlab_mock.get_issue_by_id(requesting_issue_iid)
    body = response.json()

    assert_status(response, 200)
    assert body["iid"] == requesting_issue_iid
    assert body["title"] == payload["title"]
    assert route.called


@pytest.mark.smoke
@respx.mock
async def test_get_mrs(gitlab_mock: GitLab, mrs_payload: list[dict]) -> None:
    route = respx.get(_mrs_url(gitlab_mock)).mock(
        return_value=httpx.Response(200, json=mrs_payload)
    )

    response = await gitlab_mock.get_mrs()
    body = response.json()

    assert_status(response, 200)
    assert len(body) == len(mrs_payload)
    assert body[0]["iid"] == mrs_payload[0]["iid"]
    assert body[0]["title"] == mrs_payload[0]["title"]
    assert route.called


@respx.mock
@pytest.mark.parametrize("requesting_mr_iid", [111, 444, 555])
async def test_get_mr_by_id(
    gitlab_mock: GitLab,
    mr_payload: dict,
    requesting_mr_iid: int,
) -> None:
    payload = {**mr_payload, "iid": requesting_mr_iid}
    route = respx.get(_mrs_url(gitlab_mock, requesting_mr_iid)).mock(
        return_value=httpx.Response(200, json=payload)
    )

    response = await gitlab_mock.get_mr_by_id(requesting_mr_iid)
    body = response.json()

    assert_status(response, 200)
    assert body["iid"] == requesting_mr_iid
    assert body["title"] == payload["title"]
    assert route.called
