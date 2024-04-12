-- setup_mysql_dev.sql.
-- This file is used to create the database and tables for the
-- goldenBill project.
CREATE DATABASE IF NOT EXISTS hrpro_test_db;
CREATE USER IF NOT EXISTS 'hrpro_test'@'localhost' IDENTIFIED BY 'hrpro_test_pwd';
GRANT USAGE ON *.* TO 'hrpro_test'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'hrpro_test'@'localhost';
GRANT ALL PRIVILEGES ON gb_test_db.* TO 'hrpro_test'@'localhost';
