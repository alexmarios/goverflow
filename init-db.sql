CREATE DATABASE openmetadata_db;
CREATE DATABASE airflow_db;
GRANT ALL PRIVILEGES ON DATABASE openmetadata_db TO stack_user;
GRANT ALL PRIVILEGES ON DATABASE airflow_db TO stack_user;
