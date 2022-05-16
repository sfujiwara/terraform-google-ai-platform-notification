variable "project" {
  type        = string
  description = "Google Cloud Platform project ID."
}

variable "region" {
  type        = string
  description = "Region of Cloud Functions and Cloud Storage bucket."
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

variable "label" {
  type = object({
    key   = string
    value = string
  })
  default = {
    key   = null
    value = null
  }
  description = "Statuses of jobs with label `key:value` are published to Pub/Sub. If both key and value are `null`, all jobs are the targets (for compatibility)."
}
