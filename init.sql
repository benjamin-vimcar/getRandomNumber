CREATE DATABASE IF NOT EXISTS random_number;
USE random_number;
CREATE TABLE IF NOT EXISTS users (
    email VARCHAR(320),
    password TEXT(65535),
    confirmed BOOLEAN
);
