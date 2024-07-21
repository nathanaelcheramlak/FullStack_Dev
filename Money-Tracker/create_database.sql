CREATE DATABASE IF NOT EXISTS money_tracker;
CREATE USER IF NOT EXISTS 'money_tracker_dev'@'localhost' IDENTIFIED BY 'dev';
GRANT ALL PRIVILEGES ON money_tracker_db.* TO 'money_tracker_dev'@'localhost';
FLUSH PRIVILEGES;