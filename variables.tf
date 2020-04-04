variable "region" {
  default = "ap-south-1"
}
variable "function_name" {
  default = "attach_SG_lambda_function"
}

variable "handler" {
  default = "attach_sec.handler"
}

variable "runtime" {
  default = "python3.8"
}
