from enum import Enum
from typing import Dict, Optional
from pydantic import BaseModel
from pydantic import Field


class Event(BaseModel):
    """
    Pub/Sub event pushed to Cloud Functions.
    """

    attributes: Dict = Field(
        ...,
        example={"logging.googleapis.com/timestamp": "2021-01-01T01:42:42.123456789Z"},
    )
    data: str


class JobState(Enum):
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    QUEUED = "QUEUED"


class Labels(BaseModel):
    project_id: str
    job_id: str


class Resource(BaseModel):
    labels: Labels


class JsonPayload(BaseModel):
    message: str


class Data(BaseModel):
    timestamp: str
    resource: Resource
    textPayload: Optional[str]
    jsonPayload: Optional[JsonPayload]
