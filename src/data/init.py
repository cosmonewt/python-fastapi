"""Initialize SQLite database"""

import os
from pathlib import Path
from sqlite3 import connect, Connection, Cursor, IntegrityError

conn: Connection | None = None
curs: Cursor | None = None

def get_db(name: str | None = None, reset: bool = False):
    """Connect to SQLite database file"""
    global conn, curs
    # if there is a connection...
    if conn:
        # and reset is not True...
        if not reset:
            # "do nothing" and return
            return
        # else, reset connection 
        conn = None
    # if name is empty...
    if not name:
        name = os.getenv("CRYPTID_SQLITE_DB") # shell environment variable
        top_dir = Path(__file__).resolve().parents[1] # repo top
        db_dir = top_dir / "db" # append "/db" to top_dir
        db_name = "cryptid.db"
        db_path = str(db_dir / db_name) # append db_name to db_dir
        name = os.getenv("CRYPTID_SQLITE_DB", db_path) # set as "CRYPTID_SQLITE_DB" or default to db_path
        # name = os.getenv("CRYPTID_SQLITE_DB") or db_path # catches empty strings and None
    conn = connect(name, check_same_thread=False)
    curs = conn.cursor()

get_db()

# # === DEBUG === 
# name = os.getenv("CRYPTID_SQLITE_DB")
# top_dir = Path(__file__).resolve().parents[1] # repo top
# db_dir = top_dir / "db"
# db_name = "cryptid.db"
# db_path = str(db_dir / db_name)
# name = os.getenv("CRYPTID_SQLITE_DB") or db_path 

# print(f"name: {name}")
# print(f"top_dir: {top_dir}")
# print(f"db_dir: {db_dir}")
# print(f"db_name: {db_name}")
# print(f"db_path: {db_path}")
# print(f"name os.getenv:", os.getenv("CRYPTID_SQLITE_DB", db_path))
# # === DEBUG END ===

# # get_db()

# # === DEBUG ===
# query = "SELECT * FROM creature;"
# curs.execute(query)
# print("=== DEBUG data/init.py creature query ===\n", curs.fetchall())

# query = "SELECT name FROM sqlite_master WHERE type='table';"
# curs.execute(query)
# print("=== DEBUG data/init.py sql_master query ===\n", curs.fetchall())
# # === DEBUG END ===

 