provider "google-beta" {
  project = var.project
}

module "ai_platform_notification" {
  source  = "../"
  project = var.project
}

resource "google_pubsub_subscription" "ai_platform_notification" {
  name                 = "ai-platform-notification-test"
  project              = var.project
  topic                = module.ai_platform_notification.notification_topic.id
  ack_deadline_seconds = 60
}

resource "google_pubsub_subscription" "ai_platform_log" {
  name                 = "ai-platform-log-test"
  project              = var.project
  topic                = module.ai_platform_notification.log_topic.id
  ack_deadline_seconds = 60
}
