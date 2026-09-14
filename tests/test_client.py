from __future__ import annotations

import os

import pytest

from src.gitlab_client import GitLab, assert_status

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        not os.getenv("GITLAB_TOKEN", "").strip(),
        reason="GITLAB_TOKEN не определен",
    ),
]


@pytest.mark.smoke
async def test_get_issues(gitlab: GitLab) -> None:
    response = await gitlab.get_issues()
    body = response.json()

    assert_status(response, 200)
    assert len(body) > 0
    assert "iid" in body[0]


@pytest.mark.parametrize("requesting_issue_iid", [2011, 2006, 2000])
async def test_get_issue_by_id(
    gitlab: GitLab,
    requesting_issue_iid: int,
) -> None:
    response = await gitlab.get_issue_by_id(requesting_issue_iid)
    body = response.json()

    assert_status(response, 200)
    assert body["iid"] == requesting_issue_iid


@pytest.mark.smoke
async def test_get_mrs(gitlab: GitLab) -> None:
    response = await gitlab.get_mrs()
    body = response.json()

    assert_status(response, 200)
    assert len(body) > 0
    assert "iid" in body[0]


@pytest.mark.parametrize("requesting_mr_iid", [2011, 2006, 2000])
async def test_get_mr_by_id(gitlab: GitLab, requesting_mr_iid: int) -> None:
    response = await gitlab.get_mr_by_id(requesting_mr_iid)
    body = response.json()

    assert_status(response, 200)
    assert body["iid"] == requesting_mr_iid
