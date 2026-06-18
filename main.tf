terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "6.8.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
  #Defining labels to everybody knows that is a learning project
  default_labels = {
    env     = "learning"
    owner = "joao-araujo"
    purpose = "dbt-tutorial"
  }
}

# Create the bucket to work as landing zone
resource "google_storage_bucket" "landing_zone" {
  name                     = "${var.dataset_id}-landing-zone"
  location                 = "us" # Match your BigQuery dataset location
  storage_class            = "STANDARD"
  uniform_bucket_level_access = true
  versioning {
    enabled = true
  }
}



# Create all the datasets in BigQuery

# Create the raw dataset
resource "google_bigquery_dataset" "anac_source" {
  dataset_id                  = "${var.dataset_id}_source"
  friendly_name               = "${var.dataset_id}_source"
  description                 = "Raw dataset of ANAC data"
  location                    = "us"
}

# Create the staging dataset
resource "google_bigquery_dataset" "anac_staging" {
  dataset_id                  = "${var.dataset_id}_staging"
  friendly_name               = "${var.dataset_id}_staging"
  description                 = "Staging dataset of ANAC data"
  location                    = "us"
}

# Create the intermediate dataset
resource "google_bigquery_dataset" "anac_intermediate" {
  dataset_id                  = "${var.dataset_id}_intermediate"
  friendly_name               = "${var.dataset_id}_intermediate"
  description                 = "Intermediate dataset of ANAC data"
  location                    = "us"
}

# Create the mart dataset
resource "google_bigquery_dataset" "anac_mart" {
  dataset_id                  = "${var.dataset_id}_mart"
  friendly_name               = "${var.dataset_id}_mart"
  description                 = "Mart dataset of ANAC data"
  location                    = "us"
}



# Create the service account to work in this process

resource "google_service_account" "service_account" {
  account_id   = "dbt-learning-project"
  display_name = "dbt-learning-project"
  description = "Service account to work in the entire dbt project"
}


variable "pipeline_roles" {
  type    = list(string)
  default = [
    "roles/storage.objectCreator", # Write data to GCS
    "roles/storage.objectViewer", # Read data from GCS
    "roles/bigquery.dataEditor",  # Write data into BigQuery
    "roles/bigquery.jobUser"       # Permission to actually execute BQ jobs
  ]
}

resource "google_project_iam_member" "pipeline_iam_bindings" {
  for_each = toset(var.pipeline_roles)
  project =  var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.service_account.email}"
}

