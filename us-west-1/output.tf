output "nome_instancia_region" {
    value = [for key, value in aws_instance.app_server : "nome: ${key}| id: ${value.id} - ${value.availability_zone}"]
}
output "instances" {
    value = data.aws_instances.instances
}
output "security_group_name" {
    value = [for key, value in aws_security_group.allow : [for rule in value.ingress: "nome: ${key} - description: ${rule.description} - from_port: ${rule.from_port} - to_port: ${rule.to_port} - protocol: ${rule.protocol} - cidr_blocks: ${rule.cidr_blocks[0]}"]]
}

    