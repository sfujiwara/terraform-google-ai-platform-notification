# Archive Cloud Functions' source code.
data "archive_file" "functions" {
  type        = "zip"
  source_dir  = "${path.module}/functions"
  output_path = "${path.module}/functions.zip"
}

# Cloud Storage bucket to save Cloud Functions' source code.
resource "google_storage_bucket" "functions" {
  name          = "${var.project_id}-ai-platform-notification"
  location      = "us-central1"
  project       = var.project_id
  storage_class = "REGIONAL"
}

resource "google_storage_bucket_object" "functions" {
  name   = "${data.archive_file.functions.output_md5}.zip"
  bucket = google_storage_bucket.functions.name
  source = data.archive_file.functions.output_path
}

resource "google_cloudfunctions_function" "function" {
  name                  = "ai-platform-notification"
  description           = "Cloud Functions to check AI Platform log messages."
  runtime               = "python38"
  available_memory_mb   = 128
  source_archive_bucket = google_storage_bucket.functions.name
  source_archive_object = google_storage_bucket_object.functions.name
  entry_point           = "main"
  project               = var.project_id
  region                = "us-central1"
  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = google_pubsub_topic.ai_platform_log.id
  }
  environment_variables = {
    TARGET_TOPIC = google_pubsub_topic.ai_platform_notification.id
  }
}

# Pub/Sub topic to receive AI Platform logs.
resource "google_pubsub_topic" "ai_platform_log" {
  name    = "ai-platform-log"
  project = var.project_id
}

# Pub/Sub topic to receive push notifications from Cloud Run.
resource "google_pubsub_topic" "ai_platform_notification" {
  name    = "ai-platform-notification"
  project = var.project_id
}

# Log sink to send AI Platform logs to Stackdriver Logging.
resource "google_logging_project_sink" "ai_platform_log" {
  name                   = "ai-platform-log"
  project                = var.project_id
  destination            = "pubsub.googleapis.com/${google_pubsub_topic.ai_platform_log.id}"
  filter                 = "resource.type=ml_job AND resource.labels.task_name=service"
  unique_writer_identity = true
}

resource "google_pubsub_topic_iam_member" "log_sink_sa" {
  project = google_pubsub_topic.ai_platform_log.project
  topic   = google_pubsub_topic.ai_platform_log.name
  role    = "roles/pubsub.publisher"
  member  = google_logging_project_sink.ai_platform_log.writer_identity
}
