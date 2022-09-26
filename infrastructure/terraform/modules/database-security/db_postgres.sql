CREATE DATABASE ${database_name};
CREATE USER ${database_name} WITH ENCRYPTED PASSWORD '${database_password}';
GRANT ALL PRIVILEGES ON DATABASE ${database_name} TO ${database_name};