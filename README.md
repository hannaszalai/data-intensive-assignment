# Multi-Database Manager

A web application that demonstrates multi-database connection handling with three separate SQLite databases, a unified frontend for reading and modifying data, and proper transaction processing.

## Video Demo

[![Assignment 2 Video](https://img.youtube.com/vi/Y8OYV1Y1t-c/hqdefault.jpg)](https://youtu.be/Y8OYV1Y1t-c)

## Architecture

```
            ┌──────────────┐
            │  Streamlit   │  ← Web Frontend (browser)
            │   Web UI     │
            └──────┬───────┘
                   │  user selects DB
            ┌──────▼───────┐
            │   Mediator   │  ← Routes queries to the correct DB
            │   (Python)   │
            └──┬───┬───┬───┘
               │   │   │
          ┌────┘   │   └────┐
          ▼        ▼        ▼
       hr.db  inventory.db  sales.db
```

## Databases

| Database       | File            | Table          | Columns                                    |
|----------------|-----------------|----------------|---------------------------------------------|
| HR             | `hr.db`         | `employees`    | id, name, department, role                  |
| Inventory      | `inventory.db`  | `products`     | id, product_name, stock_count, price        |
| Sales          | `sales.db`      | `transactions` | id, customer_name, amount, date             |

## Setup & Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialise the databases (creates .db files with dummy data)

```bash
python init_databases.py
```

### 3. Launch the application

```bash
streamlit run app.py --server.headless true
```

Open **http://localhost:8501** in your browser.

## Features

- **Database selector** — sidebar dropdown to switch between HR, Inventory, and Sales
- **Data viewer** — interactive table showing all records from the selected database
- **Insert form** — add new records with type-appropriate input fields
- **Edit / Delete** — select a record by ID, modify its values, or remove it
- **Transaction safety** — all writes use explicit `conn.commit()` for ACID compliance

## Files

| File                  | Purpose                                          |
|-----------------------|--------------------------------------------------|
| `requirements.txt`    | Python dependencies                              |
| `init_databases.py`   | Creates and populates the three SQLite databases  |
| `app.py`              | Streamlit application (frontend + mediator logic) |
| `hr.db`               | HR database (generated)                           |
| `inventory.db`        | Inventory database (generated)                    |
| `sales.db`            | Sales database (generated)                        |