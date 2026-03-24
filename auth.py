"""
Authentication module for EstateHub
"""
import hashlib
import secrets
import streamlit as st
from database import db
import config

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return hash_password(password) == hashed

def generate_otp() -> str:
    """Generate 6-digit OTP"""
    return str(secrets.randbelow(900000) + 100000)

def register_user(name: str, email: str, phone: str, password: str, role: str = "user") -> tuple:
    """Register a new user"""
    email = email.lower().strip()
    
    # Check if user exists
    if db.get_user_by_email(email):
        return False, "Email already registered"
    
    user_data = {
        "name": name.strip(),
        "email": email,
        "phone": phone.strip(),
        "password": hash_password(password),
        "role": role
    }
    
    try:
        user_id = db.create_user(user_data)
        return True, user_id
    except Exception as e:
        return False, str(e)

def login_user(email: str, password: str) -> tuple:
    """Login user and return user data"""
    email = email.lower().strip()
    user = db.get_user_by_email(email)
    
    if not user:
        return False, "User not found"
    
    if not user.get("is_active", True):
        return False, "Account is blocked. Contact support."
    
    if not verify_password(password, user["password"]):
        return False, "Invalid password"
    
    return True, user

def login_admin(email: str, password: str) -> tuple:
    """Login admin"""
    email = email.lower().strip()
    admin = db.get_admin_by_email(email)
    
    if not admin:
        return False, "Admin not found"
    
    if not verify_password(password, admin["password"]):
        return False, "Invalid password"
    
    return True, admin

def set_session(user: dict, role: str = None):
    """Set user session"""
    st.session_state[config.SESSION_USER] = user
    st.session_state[config.SESSION_ROLE] = role or user.get("role", "user")
    st.session_state[config.SESSION_LOGGED_IN] = True

def clear_session():
    """Clear user session"""
    for key in [config.SESSION_USER, config.SESSION_ROLE, config.SESSION_LOGGED_IN]:
        if key in st.session_state:
            del st.session_state[key]

def is_logged_in() -> bool:
    """Check if user is logged in"""
    return st.session_state.get(config.SESSION_LOGGED_IN, False)

def get_current_user() -> dict:
    """Get current logged in user"""
    return st.session_state.get(config.SESSION_USER)

def get_current_role() -> str:
    """Get current user role"""
    return st.session_state.get(config.SESSION_ROLE)

def require_login():
    """Decorator to require login"""
    if not is_logged_in():
        st.warning("Please login to access this page")
        st.stop()

def require_role(role: str):
    """Check if user has required role"""
    if get_current_role() != role:
        st.error("Access denied. Insufficient permissions.")
        st.stop()

def reset_password(email: str, new_password: str) -> tuple:
    """Reset user password"""
    email = email.lower().strip()
    user = db.get_user_by_email(email)
    
    if not user:
        return False, "Email not found"
    
    user_id = str(user.get("_id"))
    success = db.update_user(user_id, {"password": hash_password(new_password)})
    
    if success:
        return True, "Password reset successfully"
    return False, "Failed to reset password"

def verify_user_exists(email: str) -> bool:
    """Check if user exists by email"""
    email = email.lower().strip()
    return db.get_user_by_email(email) is not None
