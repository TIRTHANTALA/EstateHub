"""
EstateHub Pages Module
"""
from pages.home import render_home
from pages.login import render_login
from pages.register import render_register
from pages.properties import render_properties
from pages.property_detail import render_property_detail
from pages.dashboard import render_dashboard, render_user_dashboard, render_profile_section
from pages.owner_dashboard import render_owner_dashboard
from pages.admin_dashboard import render_admin_dashboard
from pages.about import render_about
from pages.contact import render_contact

__all__ = [
    "render_home",
    "render_login",
    "render_register",
    "render_properties",
    "render_property_detail",
    "render_dashboard",
    "render_user_dashboard",
    "render_profile_section",
    "render_owner_dashboard",
    "render_admin_dashboard",
    "render_about",
    "render_contact"
]
