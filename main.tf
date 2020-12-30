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

# Service account to push message to Cloud Run
resource "google_service_account" "pubsub_sa" {
  project    = var.project_id
  account_id = "ai-platform-notification"
}

# Pub/Sub subscription to push message to Cloud Run.
resource "google_pubsub_subscription" "ai_platform_log" {
  name                 = "ai-platform-log"
  project              = var.project_id
  topic                = google_pubsub_topic.ai_platform_log.name
  ack_deadline_seconds = 60
  push_config {
    push_endpoint = google_cloud_run_service.ai_platform_notification.status[0].url
    oidc_token {
      service_account_email = google_service_account.pubsub_sa.email
    }
  }
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

resource "google_cloud_run_service" "ai_platform_notification" {
  name     = "ai-platform-notification"
  project  = var.project_id
  location = "us-central1"

  template {
    spec {
      containers {
        image = "${var.cloud_run_image}:${var.cloud_run_image_tag}"
        env {
          name  = "THREADS"
          value = 2
        }
        env {
          name  = "WORKERS"
          value = 1
        }
        env {
          name  = "TARGET_TOPIC"
          value = google_pubsub_topic.ai_platform_notification.id
        }
      }
    }
  }
}

resource "google_cloud_run_service_iam_member" "pubsub_sa" {
  location = google_cloud_run_service.ai_platform_notification.location
  project  = google_cloud_run_service.ai_platform_notification.project
  service  = google_cloud_run_service.ai_platform_notification.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.pubsub_sa.email}"
}

resource "google_project_iam_member" "default_pubsub_sa" {
  project = var.project_id
  member  = "serviceAccount:service-${var.project_number}@gcp-sa-pubsub.iam.gserviceaccount.com"
  role    = "roles/iam.serviceAccountTokenCreator"
}
