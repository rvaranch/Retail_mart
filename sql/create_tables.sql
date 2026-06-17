-- Run this file manually in MySQL before starting the FastAPI project.
-- This project code does NOT create tables automatically.

CREATE DATABASE IF NOT EXISTS retail_mart_db;

USE retail_mart_db;

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL
);
