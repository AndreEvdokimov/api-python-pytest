from __future__ import annotations

import json
import os
from pathlib import Path

import pytest
import pytest_asyncio
from dotenv import load_dotenv

from src.gitlab_client import GitLab, env_or_default

load_dotenv()

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_fixture(name: str):
    return json.loads((FIXTURES_DIR / name).read_text(encoding="utf-8"))


@pytest.fixture
def issue_payload() -> dict:
    return load_fixture("issue.json")


@pytest.fixture
def issues_payload() -> list[dict]:
    return load_fixture("issues.json")


@pytest.fixture
def mr_payload() -> dict:
    return load_fixture("mr.json")


@pytest.fixture
def mrs_payload() -> list[dict]:
    return load_fixture("mrs.json")


@pytest_asyncio.fixture
async def gitlab_mock():
    "Клиент с фиксированным URL для мок-тестов"
    client = GitLab(
        base_url="https://gitlab.com",
        project_id="123",
        token="test-token",
    )
    yield client
    await client.aclose()


@pytest_asyncio.fixture
async def gitlab():
    token = os.getenv("GITLAB_TOKEN", "")
    
    if not token:
        pytest.skip("GITLAB_TOKEN не определен")
    
    client = GitLab(
        base_url=env_or_default("GITLAB_URL", "https://gitlab.com"),
        project_id=env_or_default("PROJECT_ID", "123"),
        token=token,
    )
    yield client
    await client.aclose()
