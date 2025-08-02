provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

# Obtener informacion del servicio de Cloud Run existente
data "google_cloud_run_service" "my_cloud_run_service" {
  name     = var.cloud_run_service_name
  location = var.gcp_region
}

# Crear el trabajo de Cloud Scheduler
resource "google_cloud_scheduler_job" "my_scheduler_job" {
  name        = "invoke-iq-paises-alberto-daily"
  description = "Invoca el servicio de Cloud Run IQ paises diariamente"
  schedule    = "0 9 * * 2,4"

  http_target {
    uri         = "https://iq-paises-998937693176.europe-west1.run.app"
    http_method = "POST" 

	headers = {
      "Content-Type" = "application/json"
    }

    oidc_token {
      service_account_email = var.scheduler_service_account_email
    }
  }

  time_zone = "Europe/Madrid"
}