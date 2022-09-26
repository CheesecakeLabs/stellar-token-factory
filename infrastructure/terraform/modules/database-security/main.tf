locals {
  services          = { for key, value in var.services_config : key => value.use_database if length(try(value.use_database, [])) > 0 }
  services_mariadb  = [for key, value in local.services : key if contains(value, "mariadb")]
  services_postgres = [for key, value in local.services : key if contains(value, "postgres")]
}

resource "random_string" "service_mariadb_passwords" {
  for_each = toset(local.services_mariadb)

  length  = 32
  special = false

}

data "template_file" "mariadb_script" {
  for_each = toset(local.services_mariadb)
  template = file("${path.module}/db_mariadb.sql")

  vars = {
    database_name     = replace(each.value, "-", "_")
    database_password = random_string.service_mariadb_passwords["${each.value}"].result
  }
}

resource "random_string" "service_postgres_passwords" {
  for_each = toset(local.services_postgres)

  length  = 32
  special = false
}

data "template_file" "postgres_script" {
  for_each = toset(local.services_postgres)
  template = file("${path.module}/db_postgres.sql")

  vars = {
    database_name     = replace(each.value, "-", "_")
    database_password = random_string.service_postgres_passwords["${each.value}"].result
  }
}