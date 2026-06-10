terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "6.8.0"
    }
  }
}

provider "google" {
  project = "data-core-platform"
  region  = "us-central1"
  zone    = "us-central1-c"
}


resource "google_bigquery_dataset" "test-dataset" {
  dataset_id                  = "test"
  friendly_name               = "test"
  description                 = "This is a test description"
  location                    = "us"
  default_table_expiration_ms = 3600000
}