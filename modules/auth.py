# modules/auth.py
import bcrypt
import streamlit as st
from database.mongodb import get_database, user_schema
from datetime import datetime

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False

def signup_user(name, email, role, organization, password):
    db = get_database()
    if db is None:
        return False, "Database connection failed."
    if db.users.find_one({"email": email.lower().strip()}):
        return False, "Email already registered."
    hashed = hash_password(password)
    schema = user_schema(name, email, role, organization, hashed)
    db.users.insert_one(schema)
    return True, "Account created successfully!"

def login_user(email, password):
    db = get_database()
    if db is None:
        return False, None, "Database connection failed."
    user = db.users.find_one({"email": email.lower().strip()})
    if not user:
        return False, None, "Email not found."
    if not verify_password(password, user["password"]):
        return False, None, "Incorrect password."
    return True, user, "Login successful!"

def get_current_user():
    return st.session_state.get("user")

def is_logged_in():
    return st.session_state.get("logged_in", False)

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def require_login():
    if not is_logged_in():
        st.session_state["page"] = "login"
        st.rerun()


