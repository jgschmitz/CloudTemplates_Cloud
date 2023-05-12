# Define provider and variables
provider "mongodbatlas" {}

variable "project_id" {
  description = "GCP project ID"
}

variable "region" {
  description = "GCP region"
  default = "us-central1"
}

variable "zone" {
  description = "GCP zone"
  default = "us-central1-a"
}

variable "network_name" {
  description = "GCP VPC network name"
}

variable "private_service_name" {
  description = "Name of the Private Service Connect service"
}

variable "mongodb_user" {
  description = "MongoDB Atlas admin username"
}

variable "mongodb_password" {
  description = "MongoDB Atlas admin password"
}

# Define VPC network
resource "google_compute_network" "vpc_network" {
  name                    = var.network_name
  auto_create_subnetworks = false
}

# Define VPC subnet
resource "google_compute_subnetwork" "vpc_subnet" {
  name                     = "${var.network_name}-subnet"
  ip_cidr_range            = "10.0.0.0/24"
  network                  = google_compute_network.vpc_network.self_link
  region                   = var.region
  private_ip_google_access = true
}

# Create Private Service Connect endpoint for MongoDB Atlas
resource "google_service_networking_connection" "private_service_connection" {
  provider                  = google-beta
  service                   = "servicenetworking.googleapis.com"
  reserved_peering_ranges   = [google_compute_subnetwork.vpc_subnet.ip_cidr_range]
  network                   = google_compute_network.vpc_network.self_link
  private_service_provider = {
    service = "mongodb-atlas.googleapis.com"
  }
}

# Define MongoDB Atlas project
resource "mongodbatlas_project" "project" {
  name = "my-mongodb-atlas-project"
}

# Define MongoDB Atlas cluster
resource "mongodbatlas_cluster" "cluster" {
  name                  = "my-mongodb-atlas-cluster"
  num_shards            = 1
  provider_name         = "GCP"
  region_name           = var.region
  instance_size_name    = "M10"
  disk_size_gb          = 10
  backup_enabled        = true
  provider_backup       = {}
  project_id            = mongodbatlas_project.project.id
  provider_cluster      = {
    provider_name   = "GCP"
    region_name     = var.region
    replication_factor = 3
    instance_size_name = "M10"
    disk_size_gb = 10
  }
}

# Create a MongoDB Atlas database user
resource "mongodbatlas_database_user" "mongodb_user" {
  username      = var.mongodb_user
  password      = var.mongodb_password
  auth_database = "admin"
  roles {
    role     = "atlasAdmin"
    database = "admin"
  }
  project_id = mongodbatlas_project.project.id
}

# Add the MongoDB Atlas database user to the cluster
resource "mongodbatlas_database_user_cluster_binding" "mongodb_user_cluster_binding" {
  username        = mongodbatlas_database_user.mongodb_user.username
  project_id      = mongodbatlas_project.project.id
  cluster_id      = mongodbatlas_cluster.cluster.id
  db_user_role    = "readWrite"
}

# Configure Private Service Connect endpoint access for MongoDB Atlas
resource "mongodbatlas_private_endpoint" "private_endpoint" {
  provider_name   = "GCP"
  region_name     = var.region
  cluster_id     
