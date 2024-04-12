-- setup_mysql_dev.sql.
-- This file is used to create the database and tables for the
-- goldenBill project.
CREATE DATABASE IF NOT EXISTS hrpro_dev_db;
CREATE USER IF NOT EXISTS 'hrpro_dev'@'localhost' IDENTIFIED BY 'hrpro_dev_pwd';
GRANT USAGE ON *.* TO 'hrpro_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'hrpro_dev'@'localhost';
GRANT ALL PRIVILEGES ON hrpro_dev_db.* TO 'hrpro_dev'@'localhost';
