output "log_topic" {
  value       = google_pubsub_topic.ai_platform_log
  description = "Pub/Sub topic name for log sink."
}

output "notification_topic" {
  value       = google_pubsub_topic.ai_platform_notification
  description = "Pub/Sub topic name for notification message."
}
