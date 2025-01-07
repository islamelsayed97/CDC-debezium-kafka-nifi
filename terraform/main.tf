# Configure the Google provider
provider "google" {
  credentials = file("terraform-sa-key.json")
  project     = var.project_id
  region      = "us-central1"
}

# Create a BigQuery dataset
resource "google_bigquery_dataset" "analytics" {
  dataset_id  = var.dataset_id
  location    = "US"
}

# Create Bigquery transactions table
resource "google_bigquery_table" "transaction_table" {
  dataset_id = var.dataset_id
  table_id   = var.table_name
  schema = file("transactions_schema.json")
}
