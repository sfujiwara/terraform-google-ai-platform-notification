from enum import Enum
from typing import Dict, Optional
from pydantic import BaseModel
from pydantic import Field


class Message(BaseModel):
    attributes: Dict = Field(
        ...,
        example={"logging.googleapis.com/timestamp": "2021-01-01T01:42:42.123456789Z"},
    )
    data: str = Field(
        ...,
        example="eyJ0aW1lc3RhbXAiOiAiIiwgInJlc291cmNlIjogeyJsYWJlbHMiOiB7ImpvYl9pZCI6ICIiLCAicHJvamVjdF9pZCI6ICIifX0sICJ0ZXh0UGF5bG9hZCI6ICJKb2IgY29tcGxldGVkIHN1Y2Nlc3NmdWxseS4ifQo=",
    )
    messageId: str = Field(..., example="1234567891234567")
    message_id: str = Field(..., example="1234567891234567")
    publishTime: str = Field(..., example="2021-01-01T01:42:42.42Z")
    publish_time: str = Field(..., example="2021-01-01T01:42:42.42Z")


class PubSubMessage(BaseModel):
    message: Message
    subscription: str = Field(
        ..., example="projects/<project-id>/subscriptions/<subscription-name>"
    )


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
