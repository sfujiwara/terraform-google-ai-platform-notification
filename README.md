# AI Platform Notification

![GitHub Actions](https://github.com/sfujiwara/terraform-google-ai-platform-notification/workflows/unit-test/badge.svg)

This is an implementation to notify status changes of AI Platform training.

Unfortunately, [AI Platform training does not support notification of status changes](https://stackoverflow.com/questions/59892910/is-there-a-way-to-be-notified-of-status-changes-in-google-ai-platform-training-j).
This module might be helpful until the notification is officially supported.

## Architecture

The architecture is as below:

<img src="img/architecture.png" width="800"/>

This Terraform module create

- Log sink to Pub/Sub topic
- Pub/Sub topic to receive the logs
  - This topic push the logs to Cloud Run service
- Cloud Run to receive message from log topic
  - Cloud Run checks AI Platform job status using the logs
- Pub/Sub topic to receive notification from Cloud Run
  - You can use this topic to know the changes of AI Platform jobs

## Message

The message published to notification topic is as below:

```json
{
  "job_id": "<AI Platform training job ID>",
  "project_id": "<Your GCP project ID>",
  "timestamp": "2020-12-23T21:02:36.069049148Z",
  "job_state": "SUCCEEDED"
}
```

`job_state` is QUEUED, SUCCEEDED, CANCELLED, or FAILED.

## Usage

```terraform
module "ai_platform_notification" {
  source              = "git::https://github.com/sfujiwara/terraform-google-ai-platform-notification.git?ref=v0.0.1"
  project_id          = "your-project-id"
  project_number      = "your-project-number"
  cloud_run_image     = "gcr.io/sfujiwara/ai-platform-notification:0.0.1"
}
```

## Docker image for Cloud Run

Docker image `gcr.io/sfujiwara/ai-platform-notification` is hosted on my Google Cloud Platform project `sfujiwara`, but there is no guarantee to be maintained.

I **strongly recommend** you to build and host your own Docker image with [`cloudrun/Dockerfile`](cloudrun/Dockerfile).
 