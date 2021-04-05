variable "project_id" {
  type        = string
  description = "Google Cloud Platform project ID."
}

variable "log_topic" {
  type        = string
  default     = "ai-platform-log"
  description = "Pub/Sub topic name for log sink."
}

variable "notification_topic" {
  type        = string
  default     = "ai-platform-notification"
  description = "Pub/Sub topic name for notification message."
}
