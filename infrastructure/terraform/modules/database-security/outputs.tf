output "service_mariadb_script" {
  value = {
    for key, value in data.template_file.mariadb_script : key => value.rendered
  }
}

output "service_postgres_script" {
  value = {
    for key, value in data.template_file.postgres_script : key => value.rendered
  }
}

output "service_mariadb_passwords" {
  value = random_string.service_mariadb_passwords
}

output "service_postgres_passwords" {
  value = random_string.service_postgres_passwords
}