provider "google-beta" {
  project = var.project_id
}

module "ai_platform_notification" {
  source         = "../"
  project_id     = var.project_id
  project_number = var.project_number
}

resource "google_pubsub_subscription" "ai_platform_log" {
  name                 = "ai-platform-notification"
  project              = var.project_id
  topic                = module.ai_platform_notification.notification_topic.id
  ack_deadline_seconds = 60
}
