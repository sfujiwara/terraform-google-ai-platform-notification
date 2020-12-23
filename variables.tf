variable "project_id" {
  type = string
}

variable "project_number" {
  type = string
}

variable "log_topic" {
  type    = string
  default = "ai-platform-log"
}

variable "notification_topic" {
  type    = string
  default = "ai-platform-notification"
}
