import sqlite3
import os

# ---------------------------------------------------------------------------
# Directory where the .db files will live
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def _db_path(name: str) -> str:
    """Return the full path for a given database file."""
    return os.path.join(BASE_DIR, name)


# ===========================================================================
# DATABASE 1 — HR  (hr.db)
# ===========================================================================
def init_hr():
    """Create the employees table and insert dummy HR records."""
    path = _db_path("hr.db")
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS employees")
    cur.execute("""
        CREATE TABLE employees (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            department  TEXT    NOT NULL,
            role        TEXT    NOT NULL
        )
    """)

    employees = [
        ("Alice Johnson",   "Engineering",      "Software Engineer"),
        ("Bob Smith",       "Engineering",      "Senior Developer"),
        ("Carol Williams",  "Marketing",        "Marketing Manager"),
        ("David Brown",     "Human Resources",  "HR Specialist"),
        ("Eva Martinez",    "Finance",          "Financial Analyst"),
        ("Frank Lee",       "Engineering",      "DevOps Engineer"),
        ("Grace Kim",       "Marketing",        "Content Strategist"),
        ("Henry Davis",     "Finance",          "Accountant"),
        ("Isla Wilson",     "Human Resources",  "Recruiter"),
        ("Jack Taylor",     "Engineering",      "QA Engineer"),
    ]

    cur.executemany(
        "INSERT INTO employees (name, department, role) VALUES (?, ?, ?)",
        employees,
    )
    conn.commit()
    conn.close()
    print(f"[OK] HR database created at {path}  ({len(employees)} rows)")


# ===========================================================================
# DATABASE 2 — Inventory  (inventory.db)
# ===========================================================================
def init_inventory():
    """Create the products table and insert dummy inventory records."""
    path = _db_path("inventory.db")
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS products")
    cur.execute("""
        CREATE TABLE products (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name  TEXT    NOT NULL,
            stock_count   INTEGER NOT NULL,
            price         REAL    NOT NULL
        )
    """)

    products = [
        ("Mechanical Keyboard",     150,  89.99),
        ("Wireless Mouse",          300,  34.50),
        ("27\" 4K Monitor",         75,   449.00),
        ("USB-C Hub",               200,  29.99),
        ("Noise-Cancelling Headset", 120, 199.95),
        ("Ergonomic Chair",          40,  549.00),
        ("Webcam HD 1080p",         180,  59.99),
        ("Laptop Stand",            250,  42.00),
    ]

    cur.executemany(
        "INSERT INTO products (product_name, stock_count, price) VALUES (?, ?, ?)",
        products,
    )
    conn.commit()
    conn.close()
    print(f"[OK] Inventory database created at {path}  ({len(products)} rows)")


# ===========================================================================
# DATABASE 3 — Sales  (sales.db)
# ===========================================================================
def init_sales():
    """Create the transactions table and insert dummy sales records."""
    path = _db_path("sales.db")
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS transactions")
    cur.execute("""
        CREATE TABLE transactions (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name  TEXT    NOT NULL,
            amount         REAL    NOT NULL,
            date           TEXT    NOT NULL
        )
    """)

    transactions = [
        ("Acme Corp",         1250.00,  "2026-09-01"),
        ("Globex Inc",        3400.50,  "2026-09-05"),
        ("Initech LLC",        899.99,  "2026-09-10"),
        ("Umbrella Co",       2100.00,  "2026-09-14"),
        ("Stark Industries",  5750.00,  "2026-09-18"),
        ("Wayne Enterprises", 4200.75,  "2026-09-22"),
        ("Cyberdyne Systems", 1680.30,  "2026-09-25"),
        ("Soylent Corp",       950.00,  "2026-09-28"),
        ("Tyrell Corp",       3125.60,  "2026-10-02"),
        ("Wonka Industries",  2875.00,  "2026-10-08"),
    ]

    cur.executemany(
        "INSERT INTO transactions (customer_name, amount, date) VALUES (?, ?, ?)",
        transactions,
    )
    conn.commit()
    conn.close()
    print(f"[OK] Sales database created at {path}  ({len(transactions)} rows)")


# ===========================================================================
# Main entry point
# ===========================================================================
if __name__ == "__main__":
    print("Initialising databases …\n")
    init_hr()
    init_inventory()
    init_sales()
    print("\nAll databases ready.")
