terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.46.0"
    }
  }
}

provider "google" {
    project = "wisdom-dev-340814"
    credentials = "${file("./credentials_gcp.json")}"
}

resource "google_bigquery_dataset" "bq_ds" {
    dataset_id = "Ruslan_Mansurov_coding_exercise"
}

resource "google_bigquery_table" "table_tf" {
    table_id = "bloomreach_task"
    dataset_id = google_bigquery_dataset.bq_ds.dataset_id
    depends_on = [google_bigquery_dataset.bq_ds]
}

locals {
  project = "wisdom-dev-340814"
}

resource "google_storage_bucket" "bucket" {
  name = "${local.project}-gcf-source1"
  location = "EU"
  uniform_bucket_level_access = true
}

resource "google_storage_bucket_object" "object1" {
  name   = "function1-source.zip"
  bucket = google_storage_bucket.bucket.name
  source = "./task1/task1-source.zip"
}

resource "google_storage_bucket_object" "object2" {
  name   = "function2-source.zip"
  bucket = google_storage_bucket.bucket.name
  source = "./task2/task2-source.zip"
}

resource "google_cloudfunctions2_function" "function1" {
  name = "function-task1"
  description = "a new function of task_1"

  build_config {
    runtime = "python310"
    entry_point = "task_1"
    source {
      storage_source {
        bucket = google_storage_bucket.bucket.name
        object = google_storage_bucket_object.object1.name
      }
    }
  }

  service_config {
    max_instance_count  = 1
    available_memory    = "256M"
    timeout_seconds     = 60
  }
}

resource "google_cloudfunctions2_function" "function2" {
  name = "function-task2"
  description = "a new function of task_2"

  build_config {
    runtime = "python310"
    entry_point = "task_2"
    source {
      storage_source {
        bucket = google_storage_bucket.bucket.name
        object = google_storage_bucket_object.object2.name
      }
    }
  }

  service_config {
    max_instance_count  = 1
    available_memory    = "256M"
    timeout_seconds     = 60
  }
}


output "function1_uri" { 
  value = google_cloudfunctions2_function.function1.service_config[0].uri
}
output "function2_uri" { 
  value = google_cloudfunctions2_function.function2.service_config[0].uri
}