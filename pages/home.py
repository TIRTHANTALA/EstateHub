"""
Home Page for EstateHub
"""
import streamlit as st
from pages.components import (
    render_navbar, render_hero_section, render_search_box,
    render_property_card, render_feature_cards, render_cta_section,
    render_testimonials, render_footer
)
from database import db

def render_home():
    """Render the home page"""
    render_navbar("Home")
    render_hero_section()
    render_search_box()
    
    # Featured Properties Section
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin: 2rem 0 1rem;">
            <div>
                <h2 style="font-size: 1.8rem; font-weight: 700; color: #1a1a2e; margin: 0;">
                    Featured Properties
                </h2>
                <p style="color: #64748b; margin: 0.25rem 0 0;">Handpicked properties for you</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col_btn = st.columns([4, 1])
    with col_btn[1]:
        if st.button("View All Properties →", use_container_width=True):
            st.session_state.page = "properties"
            st.rerun()
    
    # Get featured properties
    properties = db.get_properties(limit=6)
    
    if properties:
        cols = st.columns(3)
        for i, prop in enumerate(properties):
            with cols[i % 3]:
                render_property_card(prop)
    else:
        st.markdown("""
            <div style="text-align: center; padding: 4rem 2rem; color: #64748b;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🏢</div>
                <h3 style="color: #1a1a2e; font-weight: 600;">No properties available</h3>
                <p>Check back soon for new listings</p>
            </div>
        """, unsafe_allow_html=True)
    
    render_feature_cards()
    render_cta_section()
    render_testimonials()
    render_footer()
