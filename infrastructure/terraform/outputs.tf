output "deploy_keys" {
  sensitive = true
  value     = module.iam.deploy_keys
}
output "ecr_urls" {
  value = {
    backend  = module.backend_service.ecr_url
    frontend = module.frontend_service.ecr_url
    frontend_payment = module.frontend_payment_service.ecr_url
  }
}
output "lb_dns" {
  value = module.load_balancer.dns
}
output "postgres_password" {
  value     = module.database.postgres_password
  sensitive = true
}
output "mariadb_password" {
  value     = module.database.mariadb_password
  sensitive = true
}
output "database_scripts" {
  value = {
    "mariadb"  = module.database_security.service_mariadb_script
    "postgres" = module.database_security.service_postgres_script
  }
  sensitive = true
}
output "database_passwords" {
  value = {
    "mariadb"  = module.database_security.service_mariadb_passwords
    "postgres" = module.database_security.service_postgres_passwords
  }
  sensitive = true
}