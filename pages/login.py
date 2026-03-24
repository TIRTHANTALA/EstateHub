"""
Login Page for EstateHub
"""
import streamlit as st
from pages.components import render_navbar, render_footer
from auth import login_user, login_admin, set_session, hash_password
from utils.helpers import validate_email
from utils.email_service import generate_otp, send_otp_email, get_otp_expiry
from database import db

def render_login():
    """Render login page"""
    render_navbar("Login")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Check if in forgot password flow
    if st.session_state.get("forgot_password_step"):
        render_forgot_password()
        return
    
    _, col, _ = st.columns([1, 1.5, 1])
    
    with col:
        # Header
        st.markdown("""
            <div class="auth-header">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔐</div>
                <h2 class="auth-title">Welcome Back</h2>
                <p class="auth-subtitle">Login to your EstateHub account</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Login tabs
        tab1, tab2 = st.tabs(["👤 User / Owner", "🛡️ Admin"])
        
        with tab1:
            st.markdown("<p style='text-align: center; color: #64748b;'>login with email</p>", 
                       unsafe_allow_html=True)
            
            email = st.text_input("Email Address", placeholder="Enter your email", key="login_email")
            password = st.text_input("Password", type="password", placeholder="Enter password", key="login_pass")
            
            if st.button("🔐 Login", type="primary", use_container_width=True, key="user_login_btn"):
                if not email or not password:
                    st.error("Please fill in all fields")
                elif not validate_email(email):
                    st.error("Please enter a valid email address")
                else:
                    success, result = login_user(email, password)
                    if success:
                        set_session(result)
                        st.success("Login successful!")
                        st.session_state.page = "dashboard"
                        st.rerun()
                    else:
                        st.error(result)
            
            # Forgot Password Link
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔑 Forgot Password?", use_container_width=True):
                st.session_state.forgot_password_step = "email"
                st.rerun()
            
            st.markdown("""
                <p style="text-align: center; margin-top: 1.5rem; color: #64748b;">
                    Don't have an account? 
                </p>
            """, unsafe_allow_html=True)
            
            if st.button("Sign Up", use_container_width=True, key="goto_register"):
                st.session_state.page = "register"
                st.rerun()
        
        with tab2:
            st.markdown("<p style='text-align: center; color: #64748b;'>admin login</p>",
                       unsafe_allow_html=True)
            
            admin_email = st.text_input("Admin Email", placeholder="Enter admin email", key="admin_email")
            admin_password = st.text_input("Admin Password", type="password", 
                                          placeholder="Enter admin password", key="admin_pass")
            
            if st.button("🛡️ Admin Login", type="primary", use_container_width=True, key="admin_login_btn"):
                if not admin_email or not admin_password:
                    st.error("Please fill in all fields")
                else:
                    success, result = login_admin(admin_email, admin_password)
                    if success:
                        set_session(result, "admin")
                        st.success("Admin login successful!")
                        st.session_state.page = "admin_dashboard"
                        st.rerun()
                    else:
                        st.error(result)
    
    render_footer()

def render_forgot_password():
    """Render forgot password flow"""
    _, col, _ = st.columns([1, 1.5, 1])
    
    step = st.session_state.get("forgot_password_step", "email")
    
    with col:
        # Header
        st.markdown("""
            <div class="auth-header">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔑</div>
                <h2 class="auth-title">Reset Password</h2>
                <p class="auth-subtitle">We'll help you recover your account</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Progress indicator
        steps = ["email", "otp", "reset"]
        current_step = steps.index(step) + 1
        st.markdown(f"""
            <div style="display: flex; justify-content: center; margin-bottom: 2rem;">
                <div style="display: flex; gap: 1rem; align-items: center;">
                    <div style="width: 30px; height: 30px; border-radius: 50%; 
                        background: {'#6366f1' if current_step >= 1 else '#e2e8f0'}; 
                        color: white; display: flex; align-items: center; justify-content: center; font-size: 14px;">1</div>
                    <div style="width: 50px; height: 3px; background: {'#6366f1' if current_step >= 2 else '#e2e8f0'};"></div>
                    <div style="width: 30px; height: 30px; border-radius: 50%; 
                        background: {'#6366f1' if current_step >= 2 else '#e2e8f0'}; 
                        color: {'white' if current_step >= 2 else '#64748b'}; display: flex; align-items: center; justify-content: center; font-size: 14px;">2</div>
                    <div style="width: 50px; height: 3px; background: {'#6366f1' if current_step >= 3 else '#e2e8f0'};"></div>
                    <div style="width: 30px; height: 30px; border-radius: 50%; 
                        background: {'#6366f1' if current_step >= 3 else '#e2e8f0'}; 
                        color: {'white' if current_step >= 3 else '#64748b'}; display: flex; align-items: center; justify-content: center; font-size: 14px;">3</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if step == "email":
            render_email_step()
        elif step == "otp":
            render_otp_step()
        elif step == "reset":
            render_reset_step()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Back to login
        if st.button("← Back to Login", use_container_width=True):
            clear_forgot_password_state()
            st.rerun()
    
    render_footer()

def render_email_step():
    """Step 1: Enter email"""
    st.markdown("### Step 1: Enter Your Email")
    st.markdown("<p style='color: #64748b;'>Enter the email address associated with your account</p>", 
                unsafe_allow_html=True)
    
    email = st.text_input("Email Address", placeholder="Enter your registered email", key="reset_email_input")
    
    if st.button("📧 Send OTP", type="primary", use_container_width=True):
        if not email:
            st.error("Please enter your email address")
        elif not validate_email(email):
            st.error("Please enter a valid email address")
        else:
            # Check if user exists
            user = db.get_user_by_email(email)
            if not user:
                st.error("No account found with this email address")
            else:
                # Generate and send OTP
                otp = generate_otp()
                success, message = send_otp_email(email, otp)
                
                if success:
                    # Save OTP to database
                    db.save_otp(email, otp, get_otp_expiry())
                    st.session_state.reset_user_email = email
                    st.session_state.forgot_password_step = "otp"
                    st.success("OTP sent to your email!")
                    st.rerun()
                else:
                    st.error(message)

def render_otp_step():
    """Step 2: Verify OTP"""
    st.markdown("### Step 2: Verify OTP")
    
    email = st.session_state.get("reset_user_email", "")
    st.markdown(f"<p style='color: #64748b;'>Enter the 6-digit OTP sent to <strong>{email}</strong></p>", 
                unsafe_allow_html=True)
    
    otp = st.text_input("Enter OTP", placeholder="Enter 6-digit OTP", max_chars=6, key="forgot_otp")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Verify OTP", type="primary", use_container_width=True):
            if not otp:
                st.error("Please enter the OTP")
            elif len(otp) != 6:
                st.error("OTP must be 6 digits")
            else:
                success, message = db.verify_otp(email, otp)
                if success:
                    st.session_state.forgot_password_step = "reset"
                    st.session_state.otp_verified = True
                    st.success("OTP verified successfully!")
                    st.rerun()
                else:
                    st.error(message)
    
    with col2:
        if st.button("🔄 Resend OTP", use_container_width=True):
            otp = generate_otp()
            success, message = send_otp_email(email, otp)
            if success:
                db.save_otp(email, otp, get_otp_expiry())
                st.success("New OTP sent to your email!")
            else:
                st.error(message)

def render_reset_step():
    """Step 3: Reset password"""
    st.markdown("### Step 3: Set New Password")
    st.markdown("<p style='color: #64748b;'>Create a strong password for your account</p>", 
                unsafe_allow_html=True)
    
    new_password = st.text_input("New Password", type="password", placeholder="Enter new password", key="new_pass")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm new password", key="confirm_pass")
    
    # Password requirements
    st.markdown("""
        <div style="background: #f8fafc; padding: 12px; border-radius: 8px; margin: 10px 0;">
            <p style="font-size: 0.85rem; color: #64748b; margin: 0;">
                <strong>Password requirements:</strong><br>
                • At least 6 characters long<br>
                • Contains letters and numbers (recommended)
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔐 Reset Password", type="primary", use_container_width=True):
        if not new_password or not confirm_password:
            st.error("Please fill in all fields")
        elif len(new_password) < 6:
            st.error("Password must be at least 6 characters long")
        elif new_password != confirm_password:
            st.error("Passwords do not match")
        else:
            email = st.session_state.get("reset_user_email", "")
            
            # Update password
            hashed_password = hash_password(new_password)
            success = db.update_password(email, hashed_password)
            
            if success:
                # Clean up
                db.delete_otp(email)
                clear_forgot_password_state()
                
                st.success("Password reset successfully! Please login with your new password.")
                st.balloons()
                
                # Redirect to login after 2 seconds
                import time
                time.sleep(2)
                st.rerun()
            else:
                st.error("Failed to reset password. Please try again.")

def clear_forgot_password_state():
    """Clear all forgot password related session state"""
    keys_to_remove = ["forgot_password_step", "reset_user_email", "otp_verified"]
    for key in keys_to_remove:
        if key in st.session_state:
            del st.session_state[key]
