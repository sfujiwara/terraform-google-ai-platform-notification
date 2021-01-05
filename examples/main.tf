provider "google-beta" {
  project = var.project_id
}

module "ai_platform_notification" {
  source          = "../"
  project_id      = var.project_id
  project_number  = var.project_number
  cloud_run_image = var.cloud_run_image
}

resource "google_pubsub_subscription" "ai_platform_notification" {
  name                 = "ai-platform-notification-test"
  project              = var.project_id
  topic                = module.ai_platform_notification.notification_topic.id
  ack_deadline_seconds = 60
}

resource "google_pubsub_subscription" "ai_platform_log" {
  name                 = "ai-platform-log-test"
  project              = var.project_id
  topic                = module.ai_platform_notification.log_topic.id
  ack_deadline_seconds = 60
}
