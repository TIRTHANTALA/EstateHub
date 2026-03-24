"""
Dashboard Pages for EstateHub
"""
import streamlit as st
from pages.components import render_navbar, render_property_card, render_footer
from database import db
from auth import is_logged_in, get_current_user, get_current_role, require_login
from utils.helpers import format_price, format_date, time_ago

def render_dashboard():
    """Route to appropriate dashboard based on role"""
    require_login()
    role = get_current_role()
    
    if role == "admin":
        from pages.admin_dashboard import render_admin_dashboard
        render_admin_dashboard()
    elif role == "owner":
        from pages.owner_dashboard import render_owner_dashboard
        render_owner_dashboard()
    else:
        render_user_dashboard()

def render_user_dashboard():
    """Render user/buyer dashboard"""
    render_navbar("Dashboard")
    
    user = get_current_user()
    user_id = str(user.get("_id", ""))
    
    st.markdown(f"""
        <div style="margin-bottom: 2rem;">
            <h1 style="font-size: 2rem; font-weight: 700; color: #1a1a2e;">
                Welcome back, {user.get('name', 'User')}! 👋
            </h1>
            <p style="color: #64748b;">Manage your property search and saved listings</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Stats
    favorites = db.get_user_favorites(user_id)
    visits = db.get_visits_by_user(user_id)
    
    stat_cols = st.columns(4)
    stats = [
        ("❤️", "Saved Properties", len(favorites)),
        ("📅", "Visit Requests", len(visits)),
        ("✅", "Approved Visits", len([v for v in visits if v.get("status") == "approved"])),
        ("⏳", "Pending", len([v for v in visits if v.get("status") == "pending"]))
    ]
    
    for i, (icon, label, value) in enumerate(stats):
        with stat_cols[i]:
            st.markdown(f"""
                <div class="dashboard-card" style="text-align: center;">
                    <div style="font-size: 2rem;">{icon}</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #6366f1;">{value}</div>
                    <div style="color: #64748b; font-size: 0.9rem;">{label}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["❤️ Saved Properties", "📅 My Visits", "👤 Profile"])
    
    with tab1:
        if favorites:
            cols = st.columns(3)
            for i, prop in enumerate(favorites):
                with cols[i % 3]:
                    render_property_card(prop)
        else:
            st.info("No saved properties yet. Browse properties and click the heart icon to save.")
            if st.button("Browse Properties", type="primary"):
                st.session_state.page = "properties"
                st.rerun()
    
    with tab2:
        if visits:
            for visit in visits:
                status = visit.get("status", "pending")
                status_colors = {"pending": "#f59e0b", "approved": "#10b981", "rejected": "#ef4444"}
                
                st.markdown(f"""
                    <div class="dashboard-card" style="margin-bottom: 1rem;">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div>
                                <h4 style="font-weight: 600; margin: 0;">{visit.get('property_title', 'Property')}</h4>
                                <p style="color: #64748b; margin: 0.25rem 0;">
                                    📅 {visit.get('visit_date', '')} at {visit.get('visit_time', '')}
                                </p>
                                <p style="color: #64748b; font-size: 0.85rem; margin: 0;">
                                    Requested {time_ago(visit.get('created_at'))}
                                </p>
                            </div>
                            <span style="background: {status_colors.get(status, '#64748b')}; 
                                color: white; padding: 0.25rem 0.75rem; border-radius: 20px;
                                font-size: 0.8rem; text-transform: capitalize;">
                                {status}
                            </span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No visit requests yet. Book a visit from any property page.")
    
    with tab3:
        render_profile_section(user)
    
    render_footer()

def render_profile_section(user: dict):
    """Render user profile section"""
    st.markdown("### Profile Information")
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", value=user.get("name", ""))
        email = st.text_input("Email", value=user.get("email", ""), disabled=True)
    with col2:
        phone = st.text_input("Phone", value=user.get("phone", ""))
        role = st.text_input("Account Type", value=user.get("role", "user").capitalize(), disabled=True)
    
    if st.button("Update Profile", type="primary"):
        user_id = str(user.get("_id", ""))
        if db.update_user(user_id, {"name": name, "phone": phone}):
            # Update session
            user["name"] = name
            user["phone"] = phone
            st.session_state["user"] = user
            st.success("Profile updated successfully!")
        else:
            st.error("Failed to update profile")
    
    st.markdown("---")
    st.markdown("### Change Password")
    
    current_pass = st.text_input("Current Password", type="password", key="curr_pass")
    new_pass = st.text_input("New Password", type="password", key="new_pass")
    confirm_pass = st.text_input("Confirm New Password", type="password", key="conf_pass")
    
    if st.button("Change Password"):
        from auth import verify_password, hash_password
        if not verify_password(current_pass, user.get("password", "")):
            st.error("Current password is incorrect")
        elif len(new_pass) < 6:
            st.error("New password must be at least 6 characters")
        elif new_pass != confirm_pass:
            st.error("Passwords do not match")
        else:
            user_id = str(user.get("_id", ""))
            if db.update_user(user_id, {"password": hash_password(new_pass)}):
                st.success("Password changed successfully!")
            else:
                st.error("Failed to change password")
