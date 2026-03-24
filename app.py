"""
EstateHub - Real Estate Platform
Main Application Entry Point

A complete real estate buy & rent platform built with Python, Streamlit, and MongoDB.
"""
import streamlit as st

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="EstateHub | Buy & Rent Smartly",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Import after page config
from utils.styles import inject_css
from pages.home import render_home
from pages.login import render_login
from pages.register import render_register
from pages.properties import render_properties
from pages.property_detail import render_property_detail
from pages.dashboard import render_dashboard
from pages.owner_dashboard import render_owner_dashboard, render_edit_property
from pages.admin_dashboard import render_admin_dashboard
from pages.about import render_about
from pages.contact import render_contact

def main():
    """Main application function"""
    # Inject custom CSS
    inject_css()
    
    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = "home"
    
    # Route to appropriate page
    page = st.session_state.get("page", "home")
    
    routes = {
        "home": render_home,
        "login": render_login,
        "register": render_register,
        "properties": render_properties,
        "property_detail": render_property_detail,
        "dashboard": render_dashboard,
        "owner_dashboard": render_owner_dashboard,
        "edit_property": render_edit_property,
        "admin_dashboard": render_admin_dashboard,
        "about": render_about,
        "contact": render_contact,
    }
    
    # Render page
    render_func = routes.get(page, render_home)
    render_func()

if __name__ == "__main__":
    main()
