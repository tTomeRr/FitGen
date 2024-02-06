terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }

  }

  cloud {
    organization = "tomerc248"
    workspaces {
      name = "flex-app-cloud"
    }
  }

}


provider "aws" {
  region = var.aws-region
  access_key = var.AWS_ACCESS_KEY_ID
  secret_key = var.AWS_SECRET_ACCESS_KEY
}
