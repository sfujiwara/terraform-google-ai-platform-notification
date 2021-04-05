import base64
import json
import os
from typing import Dict, Optional
from google.cloud import pubsub_v1
from data import Event, Data, JobState, JsonPayload
from _logging import get_logger


def check_job_state(data: Data) -> Optional[JobState]:

    if isinstance(data.textPayload, str):
        if "completed successfully" in data.textPayload:
            return JobState.SUCCEEDED
        elif "failed" in data.textPayload:
            return JobState.FAILED
        elif "cancelled" in data.textPayload:
            return JobState.CANCELLED

    elif isinstance(data.jsonPayload, JsonPayload):
        if "queued" in data.jsonPayload.message:
            return JobState.QUEUED

    else:
        return None


def maybe_publish_message(message: Dict) -> None:

    logger = get_logger()

    if os.environ.get("TARGET_TOPIC"):
        publisher = pubsub_v1.PublisherClient()
        future = publisher.publish(
            topic=os.environ.get("TARGET_TOPIC"),
            data=json.dumps(message).encode("utf-8"),
        )
        logger.info("Message was published.")
    else:
        logger.info("Environment variable TARGET_TOPIC is not found.")


def main(event_dict: Dict, context) -> Dict:

    logger = get_logger()

    logger.info(json.dumps(event_dict, indent=2))
    logger.info(context)

    event = Event(**event_dict)

    data_str = base64.b64decode(event.data).decode("utf-8").strip()
    data_dict = json.loads(data_str)

    logger.info(json.dumps(data_dict, indent=2))

    data = Data(**data_dict)

    job_state = check_job_state(data)

    logger.info(f"Job state: {job_state}")

    if job_state is None:
        return {}

    output_message = {
        "job_id": data.resource.labels.job_id,
        "project_id": data.resource.labels.project_id,
        "timestamp": data.timestamp,
        "job_state": job_state.value,
    }

    logger.info(f"Output message: {json.dumps(output_message, indent=2)}")

    # Publish message to Pub/Sub topic for notification.
    maybe_publish_message(output_message)

    return {}
