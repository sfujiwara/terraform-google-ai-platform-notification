# AI Platform Notification

![GitHub Actions](https://github.com/sfujiwara/terraform-google-ai-platform-notification/actions/workflows/config.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

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
  source              = "git::https://github.com/sfujiwara/terraform-google-ai-platform-notification.git?ref=vX.X.X"
  project_id          = "your-project-id"
  project_number      = "your-project-number"
  cloud_run_image     = "gcr.io/sfujiwara/ai-platform-notification:X.X.X"
}
```

Replace `X.X.X` with the version you want to use. 

## Docker image for Cloud Run

Docker image `gcr.io/sfujiwara/ai-platform-notification` is hosted on my Google Cloud Platform project `sfujiwara`, but there is no guarantee to be maintained.

I **strongly recommend** you to build and host your own Docker image with [`cloudrun/Dockerfile`](cloudrun/Dockerfile).

## Terraform Docs

This section is automatically generated with [terraform-docs](https://github.com/terraform-docs/terraform-docs).

<!-- BEGIN_TF_DOCS -->

### Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| project\_id | Google Cloud Platform project ID. | `string` | n/a | yes |
| project\_number | Google Cloud Platform project number. | `string` | n/a | yes |
| cloud\_run\_image | Docker image used on Cloud Run. | `string` | `"gcr.io/sfujiwara/ai-platform-notification:0.0.4"` | no |
| log\_topic | Pub/Sub topic name for log sink. | `string` | `"ai-platform-log"` | no |
| notification\_topic | Pub/Sub topic name for notification message. | `string` | `"ai-platform-notification"` | no |

### Outputs

| Name | Description |
|------|-------------|
| log\_topic | Pub/Sub topic name for log sink. |
| notification\_topic | Pub/Sub topic name for notification message. |

<!-- END_TF_DOCS -->
