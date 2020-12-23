# AI Platform Notification

This is an implementation to notify status changes of AI Platform training.

Unfortunately, [AI Platform training does not support notification of status changes](https://stackoverflow.com/questions/59892910/is-there-a-way-to-be-notified-of-status-changes-in-google-ai-platform-training-j).
This module might be helpful until the notification is officially supported.

## Architecture

The architecture is as below:

<img src="img/architecture.png" width="800"/>

This Terraform module create

- Log sink to Pub/Sub topic
- Pub/Sub topic received the logs
  - This topic push the logs to Cloud Run service
- Cloud Run service received message from log topic
  - This service check AI Platform job status using the logs
- Pub/Sub topic received notification from Cloud Run
  - You can use this topic to know the changes of AI Platform jobs

## Example

```terraform
module "ai_platform_notification" {
  source         = "github.com/sfujiwara/terraform-google-ai-platform-notification"
  project_id     = "your-project-id"
  project_number = "your-project-number"
}
```
