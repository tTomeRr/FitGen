variable "aws-region" {
  type        = string
  description = "The region where the application will be deployed"
  default     = "eu-central-1"

}


variable "public_subnet_cidrs" {

  type = list(string)

  description = "Public Subnet CIDR values"

  default = ["10.0.0.0/20", "10.0.16.0/20"]

}


variable "private_subnet_cidrs" {

  type = list(string)

  description = "Private Subnet CIDR values"

  default = ["10.0.128.0/20", "10.0.144.0/20"]

}

variable "azs" {

  type = list(string)

  description = "Availability Zones"

  default = ["eu-central-1a", "eu-central-1b"]

}

variable "flex_app_image" {
  type        = string
  description = "Flask app container image uri"
  default     = "790794846345.dkr.ecr.eu-central-1.amazonaws.com/flex-repository:flex_app"
}

variable "flex_db_image" {
  type        = string
  description = "Flask DB container image uri"
  default     = "790794846345.dkr.ecr.eu-central-1.amazonaws.com/flex-repository:flex_db"
}

variable "alb_tls_cert_arn" {
  type        = string
  description = "Certificate for HTTPS"
  default     = "arn:aws:acm:eu-central-1:790794846345:certificate/6d2d9784-3e3c-4dac-bcb6-6602649500dd"
}

variable "POSTGRES_USER" {
  description = "The PostgreSQL user"
  type        = string
  sensitive   = true
}

variable "POSTGRES_PASSWORD" {
  description = "The PostgreSQL password"
  type        = string
  sensitive   = true
}

variable "POSTGRES_DB" {
  description = "The PostgreSQL database"
  type        = string
  sensitive   = true
}

variable "POSTGRES_HOST" {
  description = "The PostgreSQL host"
  type        = string
  sensitive   = true
}

variable "AWS_ACCESS_KEY_ID" {
  type = string
  default = ""
}

variable "AWS_SECRET_ACCESS_KEY" {
  type = string
  default = ""
}