terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = var.aws_region
}
   
resource "aws_vpc" "main" {
  cidr_block       =    var.vpc_cidr_block        
  instance_tenancy = "default"

  tags = {
    name = "VPC_certa${var.aws_region}"
  }
}

resource "aws_subnet" "main" {
  vpc_id     = aws_vpc.main.id
  cidr_block = cidrsubnet(aws_vpc.main.cidr_block, 8, 1)
  map_public_ip_on_launch = true

  tags = {
    Name = "Subnet"
  }
}
resource "aws_subnet" "private" {
  cidr_block              = cidrsubnet(aws_vpc.main.cidr_block, 8, 3)
  availability_zone       = data.aws_availability_zones.available.names[0]
  vpc_id                  = aws_vpc.main.id
  map_public_ip_on_launch = true

  tags = {
    Name = "Private"
  }
  depends_on = [aws_internet_gateway.gw]
}



resource "aws_subnet" "public" {
  cidr_block              = cidrsubnet(aws_vpc.main.cidr_block, 8, 2)
  availability_zone       = data.aws_availability_zones.available.names[1]
  vpc_id                  = aws_vpc.main.id
  map_public_ip_on_launch = true

  tags = {
    Name = "Public"
  }
}
resource "aws_internet_gateway" "gw" {
    vpc_id   = aws_vpc.main.id

    tags = {
        Name = "iaas_gateway"
    }
    depends_on = [aws_vpc.main]
}
resource "aws_route" "internet_access" {
    route_table_id         = aws_vpc.main.main_route_table_id
    destination_cidr_block = "0.0.0.0/0"
    gateway_id             = aws_internet_gateway.gw.id  
}