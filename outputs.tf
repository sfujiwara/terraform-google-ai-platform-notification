output "log_topic" {
  value = google_pubsub_topic.ai_platform_log
}

output "notification_topic" {
  value = google_pubsub_topic.ai_platform_notification
}
