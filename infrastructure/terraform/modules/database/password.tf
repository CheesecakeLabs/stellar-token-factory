resource "random_string" "postgres_password" {
  length  = 32
  special = false
}

resource "random_string" "mariadb_password" {
  length  = 32
  special = false
}

resource "random_string" "kong_password" {
  length  = 32
  special = false
}