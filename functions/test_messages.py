import json
import pytest
from main import check_job_state
from data import Data, JobState


@pytest.mark.parametrize(
    "filepath, result",
    [
        ("data/succeeded.json", JobState.SUCCEEDED),
        ("data/failed.json", JobState.FAILED),
        ("data/queued.json", JobState.QUEUED),
        ("data/cancelled.json", JobState.CANCELLED),
    ],
)
def test_is_succeeded(filepath: str, result: bool):

    with open(filepath) as f:
        json_payload = json.load(f)

    data = Data(**json_payload)
    job_state = check_job_state(data)

    assert job_state == result
