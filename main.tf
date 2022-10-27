variable "project_id" {
  type        = string
  description = "GCP Project ID"
}

variable "db_pass" {
  type        = string
  description = "MySQL Root Password"
}

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.63.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = "us-central1"
  zone    = "us-central1-a"
}


module "gce-container" {
  source = "terraform-google-modules/container-vm/google"
  cos_image_name = "cos-97-16919-103-49"
  

  container = {
    name = "mysql"
    image = "us-central1-docker.pkg.dev/roomr-222721/roomr-docker-repo/mysql"
    env = [
      {
        name  = "MYSQL_ROOT_PASSWORD"
        value = var.db_pass
      },
    ]
    volumeMounts = [
        {
            mountPath = "/var/lib/mysql"
            name = "mysql-volume"
            readOnly  = false
        }
    ]
    
  }
  volumes = [
        {
            name = "mysql-volume"
            hostPath = {
                path = "/var/db"
            }

        }
    ]

  restart_policy = "Always"
 
}


resource "google_compute_instance" "mysql-test-instance-1" {
    name         = "mysql-test-instance-1"
    machine_type = "e2-micro"
    zone         = "us-central1-a"
    allow_stopping_for_update = true

    labels = {
        container-vm = module.gce-container.vm_container_label
    }

    metadata = {
        gce-container-declaration = module.gce-container.metadata_value
    }

    boot_disk {
        auto_delete = true
        initialize_params {
            
            image = module.gce-container.source_image
            type = "pd-standard"
            size = 10
        }
    }
    tags = ["mysql-server"]

  network_interface {
    network = "default"
    access_config {
      network_tier = "STANDARD"
    }
  }

  service_account {
    scopes = [ "cloud-platform" ]
  }



}