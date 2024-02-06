resource "aws_vpc" "flex_app_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true

  tags = {
    Name = "flex_app_vpc"
  }
}

