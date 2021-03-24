import base64
import json
import logging
import os
import sys
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
from google.cloud.logging_v2.handlers import ContainerEngineHandler
from google.cloud import pubsub_v1


app = FastAPI()


def get_logger() -> logging.Logger:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(ContainerEngineHandler(stream=sys.stderr))

    return logger


def parse_pubsub_message(pubsub_message: Dict) -> Dict:

    data = base64.b64decode(pubsub_message["message"]["data"]).decode("utf-8").strip()
    data = json.loads(data)

    return data


def is_succeeded(json_payload: Dict) -> bool:

    if "textPayload" in json_payload:
        succeeded = "completed successfully" in json_payload["textPayload"]
        return succeeded
    else:
        return False


def is_failed(json_payload: Dict) -> bool:

    if "textPayload" in json_payload:
        failed = "failed" in json_payload["textPayload"]
        return failed
    else:
        return False


def is_queued(json_payload: Dict) -> bool:

    if "jsonPayload" in json_payload:
        queued = "queued" in json_payload["jsonPayload"]["message"]
        return queued
    else:
        return False


def is_cancelled(json_payload: Dict) -> bool:

    if "textPayload" in json_payload:
        cancelled = "cancelled" in json_payload["textPayload"]
        return cancelled
    else:
        return False


class Message(BaseModel):
    attributes: Dict
    data: str
    messageId: str
    message_id: str
    publishTime: str
    publish_time: str


class PubSubMessage(BaseModel):
    message: Message
    subscription: str


@app.post("/")
def main(pubsub_message: PubSubMessage) -> Dict:

    logger = get_logger()

    data_base64 = pubsub_message.message.data
    data: Dict = json.loads(base64.b64decode(data_base64).decode("utf-8").strip())

    logger.info(pubsub_message.json())
    logger.debug(data)

    job_id = data["resource"]["labels"]["job_id"]
    project_id = data["resource"]["labels"]["project_id"]
    timestamp = data["timestamp"]

    if is_succeeded(data):
        job_state = "SUCCEEDED"
    elif is_failed(data):
        job_state = "FAILED"
    elif is_queued(data):
        job_state = "QUEUED"
    elif is_cancelled(data):
        job_state = "CANCELLED"
    else:
        return {}

    output_message = {
        "job_id": job_id,
        "project_id": project_id,
        "timestamp": timestamp,
        "job_state": job_state,
    }

    logger.info(output_message)

    # Publish message to Pub/Sub topic for notification.
    if os.environ.get("TARGET_TOPIC"):
        publisher = pubsub_v1.PublisherClient()
        future = publisher.publish(
            topic=os.environ.get("TARGET_TOPIC"),
            data=json.dumps(output_message).encode("utf-8"),
        )
        logger.info("Message was published.")
    else:
        logger.info("Environment variable TARGET_TOPIC is not found.")

    return {}
