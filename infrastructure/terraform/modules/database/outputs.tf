output "postgres_engine" {
  value = try(aws_db_instance.postgres_db[0].engine, null)
}
output "postgres_hostname" {
  value = try(aws_db_instance.postgres_db[0].address, null)
}
output "postgres_port" {
  value = try(aws_db_instance.postgres_db[0].port, null)
}
output "postgres_username" {
  value = try(aws_db_instance.postgres_db[0].username, null)
}
output "postgres_password" {
  value = try(random_string.postgres_password.result, null)
}
output "postgres_name" {
  value = try(aws_db_instance.postgres_db[0].name, null)
}
output "mariadb_hostname" {
  value = try(aws_db_instance.mariadb_db[0].address, null)
}
output "mariadb_password" {
  value = try(random_string.mariadb_password.result, null)
}
output "kong_hostname" {
  value = try(aws_db_instance.kong[0].address, null)
}
output "kong_password" {
  value = try(random_string.kong_password.result, null)
}