import base64
import json
import logging
import os
import sys
import flask
from typing import Dict, Tuple
from google.cloud.logging_v2.handlers import ContainerEngineHandler
from google.cloud import pubsub_v1


app = flask.Flask(__name__)


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


@app.route("/", methods=["POST"])
def main() -> Tuple[str, int]:

    logger = get_logger()

    envelope: Dict = flask.request.get_json()
    data = parse_pubsub_message(envelope)

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
        return "ok", 200

    output_message = {
        "job_id": job_id,
        "project_id": project_id,
        "timestamp": timestamp,
        "job_state": job_state,
    }

    logger.info(output_message)

    # Publish message to Pub/Sub topic for notification.
    publisher = pubsub_v1.PublisherClient()
    future = publisher.publish(
        topic=os.environ.get("TARGET_TOPIC"),
        data=json.dumps(output_message).encode("utf-8"),
    )

    return "ok", 200
