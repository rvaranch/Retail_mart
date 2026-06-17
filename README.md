# Retail Mart Inventory API

This is a beginner-friendly FastAPI project using MySQL and direct SQL queries.

The goal of this project is to teach students how a Python project is modularized into different `.py` files.

## What This Project Covers

- Creating a FastAPI project in VS Code
- Using `.py` files instead of Jupyter Notebook
- Reading database details from `.env`
- Validating request body using Pydantic
- Performing MySQL operations using direct SQL queries
- Creating simple APIs for inventory management

## Project Structure

```text
retail_mart_inventory_simple/
│
├── app/
│   ├── __init__.py
│   ├── main.py          # API endpoints
│   ├── database.py      # MySQL connection code
│   └── schemas.py       # Request validation models
│
├── sql/
│   └── create_tables.sql # Table creation script, run manually in MySQL
│
├── .env                 # Database configuration
├── requirements.txt     # Required Python libraries
└── README.md            # Project running instructions
```

## Why These Files Are Separate

### `main.py`

This file contains API endpoints.

Example:

```text
POST /products
GET /products
PUT /products/{product_id}
DELETE /products/{product_id}
```

### `database.py`

This file contains only database connection logic.

Reason:

```text
If database details change, we change only this file or .env file.
```

### `schemas.py`

This file contains request validation models.

Example:

```json
{
  "name": "Rice Bag",
  "category": "Groceries",
  "price": 1200,
  "quantity": 50
}
```

FastAPI validates this request before inserting it into MySQL.

### `.env`

This file stores database details.

Reason:

```text
We should not hardcode username, password, database name directly inside Python files.
```

### `sql/create_tables.sql`

This file contains table creation SQL.

Important:

```text
The Python project does not create tables automatically.
The teacher or student should run this SQL script manually in MySQL first.
```

## Step 1: Create Virtual Environment

Open terminal inside the project folder.

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## Step 2: Install Required Libraries

```bash
pip install -r requirements.txt
```

## Step 3: Update `.env`

Open `.env` file and update your MySQL details.

Example:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=retail_mart_db
DB_PORT=3306
```

## Step 4: Create Database and Table

Open MySQL Workbench or MySQL command line.

Run the script from:

```text
sql/create_tables.sql
```

The script creates:

```text
Database: retail_mart_db
Table: products
```

## Step 5: Run FastAPI Server

From the project root folder, run:

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## APIs

## 1. Health Check

```http
GET /health
```

Response:

```json
{
  "message": "Retail Mart Inventory API is running"
}
```

## 2. Add Product

```http
POST /products
```

Request body:

```json
{
  "name": "Rice Bag",
  "category": "Groceries",
  "price": 1200,
  "quantity": 50
}
```

## 3. Get All Products

```http
GET /products
```

## 4. Get Product By ID

```http
GET /products/1
```

## 5. Update Product

```http
PUT /products/1
```

Request body:

```json
{
  "name": "Rice Bag 25KG",
  "category": "Groceries",
  "price": 1300,
  "quantity": 40
}
```

## 6. Delete Product

```http
DELETE /products/1
```

## Teaching Flow

Use this order while teaching:

```text
1. Show how code is written in Jupyter Notebook.
2. Explain why real applications use .py files.
3. Show the project folder in VS Code.
4. Explain each file responsibility.
5. Run the table creation script manually in MySQL.
6. Run FastAPI server.
7. Test APIs using Swagger or Thunder Client.
8. Show how request body is validated.
9. Show how SQL query inserts/updates/deletes data.
```

## Simple Explanation For Students

```text
Request comes from client.
FastAPI receives the request.
Pydantic validates the request body.
Python runs SQL query.
MySQL stores or returns data.
FastAPI sends response back to client.
```
