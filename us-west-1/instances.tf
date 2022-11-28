resource "aws_instance" "app_server" {
  for_each = var.instances
  ami           =  each.value.image_id
  instance_type =  each.value.instance_type 
  key_name = "public_key"
  subnet_id = aws_subnet.main.id
  vpc_security_group_ids = [for security_name in var.security_group_instances[each.key].security_names : aws_security_group.allow[security_name].id]

  tags = {
    Name = "${each.key}"
  }
}