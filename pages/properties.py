"""
Properties Listing Page for EstateHub
"""
import streamlit as st
from pages.components import render_navbar, render_property_card, render_footer
from database import db
from utils.filters import build_filter_query, get_sort_options
import config

def render_properties():
    """Render properties listing page"""
    render_navbar("Properties")
    
    # Check if coming from home page with listing filter
    if "listing_filter" in st.session_state:
        if st.session_state.listing_filter == "buy":
            st.session_state.filter_listing = "Buy"
        elif st.session_state.listing_filter == "rent":
            st.session_state.filter_listing = "Rent"
        # Clear the listing_filter after applying it
        del st.session_state.listing_filter
    
    # Check if coming from home page with search filters
    if "search_filters" in st.session_state:
        search_filters = st.session_state.search_filters
        if search_filters.get("listing_type") == "buy":
            st.session_state.filter_listing = "Buy"
        elif search_filters.get("listing_type") == "rent":
            st.session_state.filter_listing = "Rent"
        
        # Apply other search filters
        if search_filters.get("city") and search_filters["city"] != "All Cities":
            st.session_state.filter_city = search_filters["city"]
        if search_filters.get("property_type") and search_filters["property_type"] != "All Types":
            st.session_state.filter_type = search_filters["property_type"]
        if search_filters.get("budget"):
            st.session_state.filter_budget = search_filters["budget"]
        
        # Clear the search_filters after applying them
        del st.session_state.search_filters
    
    # Page header
    current_filter = st.session_state.get("filter_listing", "All")
    page_title = f"{current_filter} Properties" if current_filter != "All" else "All Properties"
    
    st.markdown(f"""
        <div style="margin-bottom: 1rem;">
            <h1 style="font-size: 2rem; font-weight: 700; color: #1a1a2e; margin: 0;">
                {page_title}
            </h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Layout: Sidebar filters + Main content
    col_filter, col_main = st.columns([1, 3])
    
    with col_filter:
        st.markdown("""
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3 style="font-weight: 600; margin: 0;">Filters</h3>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Clear All", use_container_width=True):
            st.session_state.filter_listing = "All"
            st.session_state.filter_type = "All Types"
            st.session_state.filter_city = "All Cities"
            st.session_state.filter_bedrooms = 0
            st.session_state.filter_budget = "Any"
            st.rerun()
        
        st.markdown("---")
        
        # Listing Type
        st.markdown("**Listing Type**")
        listing_type = st.radio(
            "listing_type_label",
            ["All", "Buy", "Rent"],
            key="filter_listing",
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Property Type
        st.markdown("**Property Type**")
        property_type = st.selectbox(
            "property_type_label",
            ["All Types"] + config.PROPERTY_TYPES,
            key="filter_type",
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # City
        st.markdown("**City**")
        city = st.selectbox(
            "city_label",
            ["All Cities"] + config.CITIES,
            key="filter_city",
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Bedrooms
        st.markdown("**Bedrooms**")
        bedrooms = st.radio(
            "bedrooms_label",
            [0, 1, 2, 3, 4],
            format_func=lambda x: "Any" if x == 0 else f"{x}+",
            horizontal=True,
            key="filter_bedrooms",
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Budget
        st.markdown("**Budget**")
        if listing_type == "Rent":
            budget_options = list(config.RENT_BUDGET_RANGES.keys())
        else:
            budget_options = list(config.BUDGET_RANGES.keys())
        budget = st.selectbox(
            "budget_label",
            budget_options,
            key="filter_budget",
            label_visibility="collapsed"
        )
    
    with col_main:
        # Sort and count
        sort_col1, sort_col2 = st.columns([3, 1])
        
        # Build filters
        filters = build_filter_query(
            city=city,
            property_type=property_type,
            listing_type=listing_type,
            bedrooms=bedrooms if bedrooms > 0 else None,
            budget_range=budget,
            listing_type_for_budget="rent" if listing_type == "Rent" else "buy"
        )
        
        # Get properties
        properties = db.get_properties(filters)
        
        with sort_col1:
            st.markdown(f"**Showing {len(properties)} properties**")
        
        with sort_col2:
            sort_options = get_sort_options()
            sort_by = st.selectbox(
                "Sort by",
                list(sort_options.keys()),
                label_visibility="collapsed"
            )
        
        # Apply sorting
        if sort_by == "Price: Low to High":
            properties = sorted(properties, key=lambda x: x.get("price", 0))
        elif sort_by == "Price: High to Low":
            properties = sorted(properties, key=lambda x: x.get("price", 0), reverse=True)
        
        # Display properties
        if properties:
            cols = st.columns(2)
            for i, prop in enumerate(properties):
                with cols[i % 2]:
                    render_property_card(prop)
                    st.markdown("<br>", unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="text-align: center; padding: 4rem 2rem;">
                    <div style="font-size: 4rem; margin-bottom: 1rem;">🏠❌</div>
                    <h3 style="color: #1a1a2e; font-weight: 600;">No properties found</h3>
                    <p style="color: #64748b;">Try adjusting your filters</p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("Clear Filters", type="primary"):
                st.session_state.filter_listing = "All"
                st.session_state.filter_type = "All Types"
                st.session_state.filter_city = "All Cities"
                st.session_state.filter_bedrooms = 0
                st.session_state.filter_budget = "Any"
                st.rerun()
    
    render_footer()
