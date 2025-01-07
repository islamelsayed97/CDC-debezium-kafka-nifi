# The ID of the Google Cloud project
variable "project_id" {
  description = "The ID of the Google Cloud project"
  type        = string
}

# The bigquery dataset 
variable "dataset_id" {
  description = "The bigquery dataset"
  type        = string
}

# Bigquery table
variable "table_name" {
  description = "Table to store transactions"
  type	      = string
}
