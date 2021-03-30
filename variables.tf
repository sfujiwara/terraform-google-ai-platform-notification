variable "project_id" {
  type        = string
  description = "Google Cloud Platform project ID."
}

variable "project_number" {
  type        = string
  description = "Google Cloud Platform project number."
}

variable "log_topic" {
  type    = string
  default = "ai-platform-log"
}

variable "notification_topic" {
  type    = string
  default = "ai-platform-notification"
}

variable "cloud_run_image" {
  type    = string
  default = "gcr.io/sfujiwara/ai-platform-notification:0.0.3"
}
