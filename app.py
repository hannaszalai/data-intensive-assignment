import os
import sqlite3
from datetime import date

import streamlit as st

# ---------------------------------------------------------------------------
# Paths — databases live next to this script
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_CONFIG = {
    "HR (Employees)": {
        "file": os.path.join(BASE_DIR, "hr.db"),
        "table": "employees",
        "columns": ["id", "name", "department", "role"],
        "editable": ["name", "department", "role"],       # columns the user can set
    },
    "Inventory (Products)": {
        "file": os.path.join(BASE_DIR, "inventory.db"),
        "table": "products",
        "columns": ["id", "product_name", "stock_count", "price"],
        "editable": ["product_name", "stock_count", "price"],
    },
    "Sales (Transactions)": {
        "file": os.path.join(BASE_DIR, "sales.db"),
        "table": "transactions",
        "columns": ["id", "customer_name", "amount", "date"],
        "editable": ["customer_name", "amount", "date"],
    },
}


# ===========================================================================
# Database helper functions
# ===========================================================================
def get_connection(db_path: str) -> sqlite3.Connection:
    """
    Open a connection to the specified SQLite database.
    Uses Row factory so rows behave like dicts.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def fetch_all(db_path: str, table: str) -> list[dict]:
    """Read all rows from *table* in the database at *db_path*."""
    conn = get_connection(db_path)
    rows = conn.execute(f"SELECT * FROM {table}").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def insert_row(db_path: str, table: str, data: dict) -> None:
    """
    Insert a single row into *table*.
    Uses parameterised queries for safety and conn.commit() for ACID compliance.
    """
    cols = ", ".join(data.keys())
    placeholders = ", ".join(["?"] * len(data))
    sql = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"

    conn = get_connection(db_path)
    try:
        conn.execute(sql, list(data.values()))
        conn.commit()  
    finally:
        conn.close()


def update_row(db_path: str, table: str, row_id: int, data: dict) -> None:
    """
    Update the row whose id = *row_id* in *table*.
    Uses parameterised queries and explicit commit for ACID compliance.
    """
    set_clause = ", ".join([f"{col} = ?" for col in data.keys()])
    sql = f"UPDATE {table} SET {set_clause} WHERE id = ?"

    conn = get_connection(db_path)
    try:
        conn.execute(sql, list(data.values()) + [row_id])
        conn.commit() 
    finally:
        conn.close()


def delete_row(db_path: str, table: str, row_id: int) -> None:
    """Delete the row whose id = *row_id* from *table*."""
    conn = get_connection(db_path)
    try:
        conn.execute(f"DELETE FROM {table} WHERE id = ?", (row_id,))
        conn.commit()
    finally:
        conn.close()


# ===========================================================================
# Streamlit page configuration
# ===========================================================================
st.set_page_config(
    page_title="Multi-DB Manager",
    page_icon="DB",
    layout="wide",
)

# ---------------------------------------------------------------------------
# CSS 
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    /* ---- Global typography ---- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* ---- Sidebar polish ---- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1e2f 0%, #27293d 100%);
    }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3,
    section[data-testid="stSidebar"] .stMarkdown p {
        color: #e0e0e0 !important;
    }

    /* ---- Card-like sections ---- */
    div[data-testid="stExpander"] {
        border: 1px solid rgba(128, 128, 128, 0.25);
        border-radius: 12px;
        overflow: hidden;
    }

    /* ---- Success / error banners ---- */
    .stAlert { border-radius: 8px; }

    /* ---- Section headings ---- */
    h2 {
        font-weight: 600 !important;
        letter-spacing: -0.02em;
    }
    h3 {
        font-weight: 500 !important;
        color: #4a4a5a !important;
        font-size: 1.15rem !important;
        border-bottom: 1px solid rgba(128, 128, 128, 0.15);
        padding-bottom: 0.4rem;
    }
</style>
""", unsafe_allow_html=True)

# ===========================================================================
# Sidebar — database selector
# ===========================================================================
with st.sidebar:
    st.markdown("## Multi-DB Manager")
    st.markdown("---")
    selected_db = st.selectbox(
        "Select a database",
        options=list(DB_CONFIG.keys()),
        help="Choose which database to view and modify.",
    )
    cfg = DB_CONFIG[selected_db]
    st.markdown("---")
    st.caption(f"**Database file:** `{os.path.basename(cfg['file'])}`")
    st.caption(f"**Table:** `{cfg['table']}`")

# ===========================================================================
# Main area — heading
# ===========================================================================
st.title(selected_db)
st.markdown("Browse, add, and edit records in the selected database.")

# ---------------------------------------------------------------------------
# Check that the DB file exists
# ---------------------------------------------------------------------------
if not os.path.exists(cfg["file"]):
    st.error(
        f"Database file **{cfg['file']}** not found.  \n"
        "Run `python init_databases.py` first to create and populate the databases."
    )
    st.stop()

# ===========================================================================
# Section 1 — Data Viewer
# ===========================================================================
st.subheader("Data Viewer")
rows = fetch_all(cfg["file"], cfg["table"])
if rows:
    st.dataframe(rows, width="stretch", hide_index=True)
else:
    st.info("No records found in this table.")

# ===========================================================================
# Section 2 — Add New Record
# ===========================================================================
st.markdown("---")
st.subheader("Add New Record")

with st.form(key="insert_form", clear_on_submit=True):
    new_data: dict = {}

    # Build input fields dynamically based on the schema
    cols_ui = st.columns(len(cfg["editable"]))
    for idx, col_name in enumerate(cfg["editable"]):
        with cols_ui[idx]:
            if col_name in ("stock_count",):
                new_data[col_name] = st.number_input(
                    col_name.replace("_", " ").title(),
                    min_value=0, step=1, key=f"new_{col_name}",
                )
            elif col_name in ("price", "amount"):
                new_data[col_name] = st.number_input(
                    col_name.replace("_", " ").title(),
                    min_value=0.0, step=0.01, format="%.2f",
                    key=f"new_{col_name}",
                )
            elif col_name == "date":
                new_data[col_name] = st.date_input(
                    "Date", value=date.today(), key=f"new_{col_name}",
                ).isoformat()
            else:
                new_data[col_name] = st.text_input(
                    col_name.replace("_", " ").title(), key=f"new_{col_name}",
                )

    submitted = st.form_submit_button("Insert Record")
    if submitted:
        # Basic validation: text fields must not be empty
        text_fields = [k for k in new_data if isinstance(new_data[k], str) and k != "date"]
        if any(new_data[k].strip() == "" for k in text_fields):
            st.error("Please fill in all text fields before inserting.")
        else:
            insert_row(cfg["file"], cfg["table"], new_data)
            st.success("Record inserted successfully!")
            st.rerun()                     # refresh the data viewer

# ===========================================================================
# Section 3 — Edit Existing Record
# ===========================================================================
st.markdown("---")
st.subheader("Edit Existing Record")

if rows:
    # Let the user pick a row by its ID
    row_ids = [r["id"] for r in rows]
    chosen_id = st.selectbox("Select record ID to edit", row_ids, key="edit_id")

    # Find the matching row to pre-fill the form
    current = next(r for r in rows if r["id"] == chosen_id)

    with st.form(key="update_form"):
        upd_data: dict = {}
        cols_ui2 = st.columns(len(cfg["editable"]))
        for idx, col_name in enumerate(cfg["editable"]):
            with cols_ui2[idx]:
                if col_name in ("stock_count",):
                    upd_data[col_name] = st.number_input(
                        col_name.replace("_", " ").title(),
                        value=int(current[col_name]),
                        min_value=0, step=1, key=f"upd_{col_name}",
                    )
                elif col_name in ("price", "amount"):
                    upd_data[col_name] = st.number_input(
                        col_name.replace("_", " ").title(),
                        value=float(current[col_name]),
                        min_value=0.0, step=0.01, format="%.2f",
                        key=f"upd_{col_name}",
                    )
                elif col_name == "date":
                    upd_data[col_name] = st.date_input(
                        "Date",
                        value=date.fromisoformat(current[col_name]),
                        key=f"upd_{col_name}",
                    ).isoformat()
                else:
                    upd_data[col_name] = st.text_input(
                        col_name.replace("_", " ").title(),
                        value=str(current[col_name]),
                        key=f"upd_{col_name}",
                    )

        col_btn1, col_btn2, _ = st.columns([1, 1, 4])
        with col_btn1:
            update_clicked = st.form_submit_button("Update Record")
        with col_btn2:
            delete_clicked = st.form_submit_button("Delete Record")

        if update_clicked:
            update_row(cfg["file"], cfg["table"], chosen_id, upd_data)
            st.success(f"Record #{chosen_id} updated successfully!")
            st.rerun()

        if delete_clicked:
            delete_row(cfg["file"], cfg["table"], chosen_id)
            st.success(f"Record #{chosen_id} deleted.")
            st.rerun()
else:
    st.info("No records to edit — add some first using the form above.")
