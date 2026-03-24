"""
Registration Page for EstateHub
"""
import streamlit as st
from pages.components import render_navbar, render_footer
from auth import register_user, set_session, login_user
from utils.helpers import validate_email, validate_phone

def render_register():
    """Render registration page"""
    render_navbar("Register")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    _, col, _ = st.columns([1, 1.5, 1])
    
    with col:
        # Header
        st.markdown("""
            <div class="auth-header">
                <h2 class="auth-title">Create Account</h2>
                <p class="auth-subtitle">Join EstateHub today</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<p style='text-align: center; color: #64748b;'>register with email</p>",
                   unsafe_allow_html=True)
        
        # Form fields
        name = st.text_input("Full Name", placeholder="Enter your full name")
        email = st.text_input("Email Address", placeholder="Enter your email")
        phone = st.text_input("Phone Number", placeholder="Enter your phone number")
        
        # Role selection
        default_role = st.session_state.get("register_as", "user")
        role_options = ["Buy / Rent Property", "List Property (Owner)"]
        role_index = 1 if default_role == "owner" else 0
        role_selection = st.selectbox("I want to", role_options, index=role_index)
        role = "owner" if "List" in role_selection else "user"
        
        col1, col2 = st.columns(2)
        with col1:
            password = st.text_input("Password", type="password", placeholder="Create password")
        with col2:
            confirm_password = st.text_input("Confirm Password", type="password", 
                                            placeholder="Confirm password")
        
        agree = st.checkbox("I agree to the Terms of Service and Privacy Policy")
        
        if st.button("📝 Create Account", type="primary", use_container_width=True):
            # Validation
            errors = []
            if not name or len(name) < 2:
                errors.append("Please enter a valid name")
            if not validate_email(email):
                errors.append("Please enter a valid email address")
            if not validate_phone(phone):
                errors.append("Please enter a valid 10-digit phone number")
            if len(password) < 6:
                errors.append("Password must be at least 6 characters")
            if password != confirm_password:
                errors.append("Passwords do not match")
            if not agree:
                errors.append("Please agree to the Terms of Service")
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                success, result = register_user(name, email, phone, password, role)
                if success:
                    st.success("Account created successfully!")
                    # Auto login
                    login_success, user = login_user(email, password)
                    if login_success:
                        set_session(user)
                        st.session_state.page = "dashboard"
                        st.rerun()
                else:
                    st.error(result)
        
        st.markdown("""
            <p style="text-align: center; margin-top: 1.5rem; color: #64748b;">
                Already have an account?
            </p>
        """, unsafe_allow_html=True)
        
        if st.button("Login", use_container_width=True, key="goto_login"):
            st.session_state.page = "login"
            st.rerun()
    
    render_footer()
