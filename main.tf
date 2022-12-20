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
    credentials = "${file("credentials_gcp.json")}"
}

resource "google_bigquery_dataset" "bq_ds" {
    dataset_id = "Ruslan_Mansurov_coding_exercise"
}

resource "google_bigquery_table" "table_tf" {
    table_id = "bloomreach_task"
    dataset_id = google_bigquery_dataset.bq_ds.dataset_id
    depends_on = [google_bigquery_dataset.bq_ds]
}


# Push docker image to Google Artifact Registry (can use GitHub Actions)
# Create service on Google Cloud Run 
# that run docker image triggered by link (HTTP-request)
# that in turn invoke my Python functions (ETL jobs)