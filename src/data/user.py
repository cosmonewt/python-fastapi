from .init import (conn, curs, get_db, IntegrityError)
from model.user import User
from error import Missing, Duplicate

curs.execute("""CREATE TABLE IF NOT EXISTS user(name TEXT PRIMARY KEY, hash TEXT);""")
curs.execute("""CREATE TABLE IF NOT EXISTS xuser(name TEXT PRIMARY KEY, hash TEXT);""")

def row_to_model(row: tuple) -> User:
    name, hash = row
    return User(name=name, hash=hash)

def model_to_dict(user: User) -> dict:
    return user.model_dump()

def get_one(name: str, table: str = "user") -> User:
    # Only use validated and hard-coded table names for query, to avoid sql injection risks.
    # Do not dynamically accept external user inputs.
    qry = f"SELECT * FROM {table} WHERE name=:name;" 
    params = {"table": table, "name": name}
    curs.execute(qry, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"User {name} not found")

def get_all() -> list[User]:
    qry = "SELECT * FROM user;"
    curs.execute(qry)
    return [row_to_model(row) for row in curs.fetchall()]

def create(user: User, table: str = "user"):
    """Add <user> to user or xuser table"""
    qry = f"""INSERT INTO {table} (name, hash) VALUES (:name, :hash);"""
    params = model_to_dict(user)
    try:
        curs.execute(qry, params)
    except IntegrityError:
        raise Duplicate(msg=f"{table}: user {user.name} already exists")
    return get_one(user.name, table)

def modify(name: str, user: User) -> User:
    qry = """UPDATE user SET 
             name=:name, 
             hash=:hash 
             WHERE name=:name0;"""
    params = {
        "name": user.name,
        "hash": user.hash,
        "name0": name
    }
    curs.execute(qry, params)
    if curs.rowcount == 1:
        return get_one(user.name)
    else:
        raise Missing(msg=f"User {name} not found")
    
def delete(name: str) -> bool:
    """Drop user with <name> from user table, add to xuser table"""
    user = get_one(name)
    qry = "DELETE FROM user WHERE name=:name;"
    params = {"name": name}
    curs.execute(qry, params)
    if curs.rowcount != 1:
        raise Missing(msg=f"User {name} not found")
    create(user, table="xuser") 




