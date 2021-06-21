variable "cloudwatch_group" {
  type = string
  default = "stock-service"
}

variable "name_prefix" {
  description = "Name prefix of each resources"
  type = string
  default = "stock-service"
}

variable "IMAGE_VERSION" {
  type = string
}

variable "FUGLE_API_TOKEN" {
  type = string
  default = "fugle_api_token"
}
