variable "aws_access_key" {
    type = string
    sensitive = true
}

variable "aws_secret_key" {
    type = string
    sensitive = true
}

variable "aws-region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "ami" {
  description = "AMI ID"
  type        = string
  default = "ami-0ee23bfc74a881de5"
}

variable "security_groups" {
  description = "Security groups"
  type = map(object({
    security_name = string
    security_description = string
    security_ingress = list(map(object({
      description = string
      from_port = number
      to_port = number
      protocol = string
      ipv6_cidr_blocks = list(string)
      prefix_list_ids = list(string)
      self = bool
      security_groups = list(string)
      cidr_blocks = list(string)
    })))
  }))
}

variable "instances" {
  description = "Instances"
  type        = map(object({
    instance_name = string
    instance_type = string
    aws-region = string
    security_name = string
  }))
}

variable "users" {
  type = list(object({
    username = string
    restrictions = object ({
      restriction_name = string
      actions = list(string)
      resources = list(string)
    })
  }))
}