import json
import pytest
from server.main import is_failed
from server.main import is_queued
from server.main import is_succeeded


@pytest.mark.parametrize(
    "filepath, result",
    [
        ("data/succeeded.json", True),
        ("data/failed.json", False),
        ("data/queued.json", False),
    ],
)
def test_is_succeeded(filepath: str, result: bool):

    with open(filepath) as f:
        json_payload = json.load(f)

    assert is_succeeded(json_payload) == result


@pytest.mark.parametrize(
    "filepath, result",
    [
        ("data/succeeded.json", False),
        ("data/failed.json", True),
        ("data/queued.json", False),
    ],
)
def test_is_failed(filepath: str, result: bool):

    with open(filepath) as f:
        json_payload = json.load(f)

    assert is_failed(json_payload) == result


@pytest.mark.parametrize(
    "filepath, result",
    [
        ("data/succeeded.json", False),
        ("data/failed.json", False),
        ("data/queued.json", True),
    ],
)
def test_is_queued(filepath: str, result: bool):

    with open(filepath) as f:
        json_payload = json.load(f)

    assert is_queued(json_payload) == result
