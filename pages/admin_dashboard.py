"""
Admin Dashboard for EstateHub
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pages.components import render_navbar, render_footer
from database import db
from auth import require_login, require_role, get_current_user
from utils.helpers import format_price, format_date, time_ago, get_property_image_placeholder
import config

def render_admin_dashboard():
    """Render admin dashboard"""
    render_navbar("Admin")
    require_login()
    require_role("admin")
    
    st.markdown("""
        <div style="margin-bottom: 2rem;">
            <h1 style="font-size: 2rem; font-weight: 700; color: #1a1a2e;">
                Admin Dashboard 🛡️
            </h1>
            <p style="color: #64748b;">Manage platform, verify properties, and monitor users</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Get analytics
    analytics = db.get_analytics()
    
    # Stats
    stat_cols = st.columns(4)   
    stats = [
        ("👥", "Total Users", analytics.get("total_users", 0), "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"),
        ("🏠", "Properties", analytics.get("total_properties", 0), "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"),
        ("✅", "Verified", analytics.get("verified_properties", 0), "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"),
        ("⏳", "Pending", analytics.get("pending_properties", 0), "linear-gradient(135deg, #fa709a 0%, #fee140 100%)")
    ]
    
    for i, (icon, label, value, gradient) in enumerate(stats):
        with stat_cols[i]:
            st.markdown(f"""
                <div style="background: {gradient}; border-radius: 16px; padding: 1.5rem; color: white;">
                    <div style="display: flex; align-items: center; gap: 0.75rem;">
                        <span style="font-size: 2rem;">{icon}</span>
                        <div>
                            <div style="font-size: 2rem; font-weight: 700;">{value}</div>
                            <div style="opacity: 0.9;">{label}</div>
                        </div>
                    </div>
                </div>  
            """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Pending Properties", "✅ All Properties", "👥 Users", "📊 Analytics"])
    
    with tab1:
        render_pending_properties()
    
    with tab2:
        render_all_properties()
    
    with tab3:
        render_users_management()
    
    with tab4:
        render_analytics(analytics)
    
    render_footer()

def render_pending_properties():
    """Render pending properties for verification"""
    properties = db.get_all_properties()
    pending = [p for p in properties if not p.get("verified")]
    
    if not pending:
        st.success("No pending properties to verify! 🎉")
        return
    
    st.markdown(f"**{len(pending)} properties pending verification**")
    
    for prop in pending:
        prop_id = str(prop.get("_id", ""))
        owner = db.get_user_by_id(prop.get("owner_id")) if prop.get("owner_id") else None
        
        col1, col2 = st.columns([4, 1])
        
        with col1:
            image = prop.get("image") or get_property_image_placeholder(prop.get("property_type", "Flat"))
            st.markdown(f"""
                <div class="dashboard-card" style="display: flex; gap: 1.5rem;margin-bottom: 2rem;">
                    <img src="{image}" style="width: 150px; height: 110px; border-radius: 12px; object-fit: cover;"
                        onerror="this.src='{get_property_image_placeholder(prop.get('property_type', 'Flat'))}'">
                    <div style="flex: 1;">
                        <h4 style="font-weight: 600; margin: 0;">{prop.get('title', 'Property')}</h4>
                        <p style="color: #64748b; margin: 0.25rem 0;">📍 {prop.get('city', '')} | 🏠 {prop.get('property_type', '')}</p>
                        <p style="font-weight: 600; color: #6366f1; margin: 0.5rem 0;">
                            {format_price(prop.get('price', 0), prop.get('listing_type', 'buy'))}
                        </p>
                        <p style="color: #64748b; font-size: 0.85rem; margin: 0;">
                            Owner: {owner.get('name', 'Unknown') if owner else 'Unknown'} | 
                            Listed: {time_ago(prop.get('created_at'))}
                        </p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button("👁️ View Details", key=f"view_{prop_id}", use_container_width=True):
                st.session_state.admin_view_property_id = prop_id
                st.rerun()
            
            if st.button("✅ Verify", key=f"verify_{prop_id}", use_container_width=True, type="primary"):
                db.verify_property(prop_id)
                st.success("Property verified!")
                st.rerun()
            
            if st.button("🗑️ Delete", key=f"del_admin_{prop_id}", use_container_width=True):
                db.delete_property(prop_id)
                st.rerun()
    
    # Property Detail Modal
    if st.session_state.get("admin_view_property_id"):
        render_property_detail_modal(st.session_state.admin_view_property_id)

def render_property_detail_modal(property_id: str):
    """Render property details in admin view"""
    prop = db.get_property_by_id(property_id)
    if not prop:
        return
    
    owner = db.get_user_by_id(prop.get("owner_id")) if prop.get("owner_id") else None
    
    st.markdown("---")
    st.markdown("### 📋 Property Details")
    
    # Close button
    if st.button("✕ Close Details", key="close_details"):
        st.session_state.admin_view_property_id = None
        st.rerun()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Images
        images = prop.get("images", [])
        main_image = prop.get("image") or (images[0] if images else None) or get_property_image_placeholder(prop.get("property_type", "Flat"))
        
        if main_image.startswith("data:image"):
            st.markdown(f'<img src="{main_image}" style="width: 100%; max-height: 300px; object-fit: cover; border-radius: 12px;">', unsafe_allow_html=True)
        else:
            st.markdown(f'<img src="{main_image}" style="width: 100%; max-height: 300px; object-fit: cover; border-radius: 12px;" onerror="this.src=\'{get_property_image_placeholder(prop.get("property_type", "Flat"))}\'">', unsafe_allow_html=True)
        
        # Show all images count
        if images and len(images) > 1:
            st.caption(f"📷 {len(images)} images uploaded")
        
        st.markdown(f"### {prop.get('title', 'Property')}")
        st.markdown(f"**Description:** {prop.get('description', 'No description')}")
        
        # Amenities
        amenities = prop.get("amenities", [])
        if amenities:
            st.markdown("**Amenities:**")
            amenities_html = " ".join([f'<span style="background: #f0f1ff; color: #6366f1; padding: 4px 10px; border-radius: 15px; font-size: 12px; margin-right: 5px;">✓ {a}</span>' for a in amenities])
            st.markdown(amenities_html, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### Property Info")
        info_items = [
            ("💰 Price", format_price(prop.get('price', 0), prop.get('listing_type', 'buy'))),
            ("📍 City", prop.get('city', 'N/A')),
            ("🏠 Type", prop.get('property_type', 'N/A')),
            ("📋 Listing", prop.get('listing_type', 'buy').capitalize()),
            ("🛏️ Bedrooms", prop.get('bedrooms', 0)),
            ("🚿 Bathrooms", prop.get('bathrooms', 0)),
            ("📐 Area", f"{prop.get('area', 0)} sq.ft"),
            ("🪑 Furnishing", prop.get('furnishing', 'N/A')),
        ]
        
        for label, value in info_items:
            st.markdown(f"""
                <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #e2e8f0;">
                    <span style="color: #64748b;">{label}</span>
                    <span style="font-weight: 500;">{value}</span>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### Owner Details")
        if owner:
            st.markdown(f"""
                <div style="background: #f8fafc; padding: 15px; border-radius: 10px;">
                    <div style="font-weight: 600;">👤 {owner.get('name', 'Unknown')}</div>
                    <div style="color: #64748b; font-size: 0.9rem;">📧 {owner.get('email', 'N/A')}</div>
                    <div style="color: #64748b; font-size: 0.9rem;">📞 {owner.get('phone', 'N/A')}</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Action buttons
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("✅ Approve", key="modal_verify", use_container_width=True, type="primary"):
                db.verify_property(property_id)
                st.session_state.admin_view_property_id = None
                st.success("Property verified!")
                st.rerun()
        with col_b:
            if st.button("❌ Reject", key="modal_delete", use_container_width=True):
                db.delete_property(property_id)
                st.session_state.admin_view_property_id = None
                st.rerun()
    
    st.markdown("---")

def render_all_properties():
    """Render all properties"""
    properties = db.get_all_properties()
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_city = st.selectbox("Filter by City", ["All"] + config.CITIES, key="admin_city_filter")
    with col2:
        filter_status = st.selectbox("Filter by Status", ["All", "Verified", "Pending"], key="admin_status_filter")
    with col3:
        filter_type = st.selectbox("Filter by Type", ["All"] + config.PROPERTY_TYPES, key="admin_type_filter")
    
    # Apply filters
    filtered = properties
    if filter_city != "All":
        filtered = [p for p in filtered if p.get("city") == filter_city]
    if filter_status == "Verified":
        filtered = [p for p in filtered if p.get("verified")]
    elif filter_status == "Pending":
        filtered = [p for p in filtered if not p.get("verified")]
    if filter_type != "All":
        filtered = [p for p in filtered if p.get("property_type") == filter_type]
    
    st.markdown(f"**Showing {len(filtered)} of {len(properties)} properties**")
    
    for prop in filtered:
        prop_id = str(prop.get("_id", ""))
        verified = prop.get("verified", False)
        
        col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
        
        with col1:
            st.markdown(f"""
                <div class="dashboard-card">
                    <div style="display: flex; justify-content: space-between;">
                        <div>
                            <h4 style="font-weight: 600; margin: 0;">{prop.get('title', 'Property')}</h4>
                            <p style="color: #64748b; margin: 0.25rem 0;">
                                📍 {prop.get('city', '')} | {format_price(prop.get('price', 0), prop.get('listing_type', 'buy'))}
                            </p>
                        </div>
                        {"<span class='verified-badge'>✓ Verified</span>" if verified else "<span class='pending-badge'>Pending</span>"}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button("👁️ View", key=f"view_all_{prop_id}", use_container_width=True):
                st.session_state.page = "property_detail"
                st.session_state.property_id = prop_id
                st.rerun()
        
        with col3:
            if not verified:
                if st.button("✅ Verify", key=f"v_{prop_id}", use_container_width=True):
                    db.verify_property(prop_id)
                    st.rerun()
        
        with col4:
            if st.button("🗑️", key=f"d_{prop_id}", use_container_width=True):
                db.delete_property(prop_id)
                st.rerun()

def render_users_management():
    """Render users management"""
    users = db.get_all_users()
    
    # Filter
    col1, col2 = st.columns(2)
    with col1:
        role_filter = st.selectbox("Filter by Role", ["All", "user", "owner"], key="user_role_filter")
    with col2:
        status_filter = st.selectbox("Filter by Status", ["All", "Active", "Blocked"], key="user_status_filter")
    
    filtered = users
    if role_filter != "All":
        filtered = [u for u in filtered if u.get("role") == role_filter]
    if status_filter == "Active":
        filtered = [u for u in filtered if u.get("is_active", True)]
    elif status_filter == "Blocked":
        filtered = [u for u in filtered if not u.get("is_active", True)]
    
    st.markdown(f"**{len(filtered)} users**")
    
    for user in filtered:
        user_id = str(user.get("_id", ""))
        is_active = user.get("is_active", True)
        
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.markdown(f"""
                <div class="dashboard-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="display: flex; align-items: center; gap: 1rem;">
                            <div style="width: 45px; height: 45px; border-radius: 50%;
                                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                display: flex; align-items: center; justify-content: center;
                                color: white; font-weight: 600;">
                                {user.get('name', 'U')[0].upper()}
                            </div>
                            <div>
                                <h4 style="font-weight: 600; margin: 0;">{user.get('name', 'User')}</h4>
                                <p style="color: #64748b; margin: 0; font-size: 0.85rem;">
                                    {user.get('email', '')} | 📞 {user.get('phone', '')}
                                </p>
                            </div>
                        </div>
                        <div style="display: flex; gap: 0.5rem; align-items: center;">
                            <span style="background: #f0f1ff; color: #6366f1; padding: 0.2rem 0.6rem;
                                border-radius: 6px; font-size: 0.75rem; text-transform: capitalize;">
                                {user.get('role', 'user')}
                            </span>
                            <span style="background: {'#dcfce7' if is_active else '#fee2e2'};
                                color: {'#16a34a' if is_active else '#dc2626'}; padding: 0.2rem 0.6rem;
                                border-radius: 6px; font-size: 0.75rem;">
                                {'Active' if is_active else 'Blocked'}
                            </span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if is_active:
                if st.button("🚫 Block", key=f"block_{user_id}", use_container_width=True):
                    db.block_user(user_id)
                    st.rerun()
            else:
                if st.button("✅ Unblock", key=f"unblock_{user_id}", use_container_width=True):
                    db.unblock_user(user_id)
                    st.rerun()

def render_analytics(analytics: dict):
    """Render analytics section"""
    st.markdown("### Platform Analytics")
    
    # User stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class="dashboard-card" style="text-align: center;">
                <div style="font-size: 2rem;">👥</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #6366f1;">
                    {}</div>
                <div style="color: #64748b;">Total Users</div>
            </div>
        """.format(analytics.get("total_users", 0)), unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="dashboard-card" style="text-align: center;">
                <div style="font-size: 2rem;">🏠</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #6366f1;">
                    {}</div>
                <div style="color: #64748b;">Property Owners</div>
            </div>
        """.format(analytics.get("total_owners", 0)), unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="dashboard-card" style="text-align: center;">
                <div style="font-size: 2rem;">🔍</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #6366f1;">
                    {}</div>
                <div style="color: #64748b;">Buyers/Tenants</div>
            </div>
        """.format(analytics.get("total_buyers", 0)), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts Section
    st.markdown("### 📊 Visual Analytics")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Pie Chart - Property Verification Status
        st.markdown("#### Property Status")
        verified = analytics.get("verified_properties", 0)
        pending = analytics.get("pending_properties", 0)
        
        if verified > 0 or pending > 0:
            pie_data = pd.DataFrame({
                'Status': ['Verified', 'Pending'],
                'Count': [verified, pending]
            })
            
            fig_pie = px.pie(
                pie_data, 
                values='Count', 
                names='Status',
                color='Status',
                color_discrete_map={'Verified': '#10b981', 'Pending': '#f59e0b'},
                hole=0.4
            )
            fig_pie.update_layout(
                showlegend=True,
                height=300,
                margin=dict(l=20, r=20, t=30, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No property data available for chart")
    
    with chart_col2:
        # Bar Chart - Properties by City
        st.markdown("#### Properties by City")
        popular_cities = analytics.get("popular_cities", [])
        
        if popular_cities:
            cities = [city.get('_id', 'Unknown') for city in popular_cities[:6]]
            counts = [city.get('count', 0) for city in popular_cities[:6]]
            
            bar_data = pd.DataFrame({
                'City': cities,
                'Properties': counts
            })
            
            fig_bar = px.bar(
                bar_data,
                x='City',
                y='Properties',
                color='Properties',
                color_continuous_scale=['#818cf8', '#6366f1', '#4f46e5']
            )
            fig_bar.update_layout(
                showlegend=False,
                height=300,
                margin=dict(l=20, r=20, t=30, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title="",
                yaxis_title="Properties"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No city data available for chart")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # User Distribution Pie Chart
    chart_col3, chart_col4 = st.columns(2)
    
    with chart_col3:
        st.markdown("#### User Distribution")
        total_owners = analytics.get("total_owners", 0)
        total_buyers = analytics.get("total_buyers", 0)
        
        if total_owners > 0 or total_buyers > 0:
            user_data = pd.DataFrame({
                'Type': ['Property Owners', 'Buyers/Tenants'],
                'Count': [total_owners, total_buyers]
            })
            
            fig_users = px.pie(
                user_data,
                values='Count',
                names='Type',
                color='Type',
                color_discrete_map={'Property Owners': '#6366f1', 'Buyers/Tenants': '#8b5cf6'}
            )
            fig_users.update_layout(
                showlegend=True,
                height=300,
                margin=dict(l=20, r=20, t=30, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_users, use_container_width=True)
        else:
            st.info("No user data available for chart")
    
    with chart_col4:
        # Listing Type Bar Chart
        st.markdown("#### Listing Type")
        all_properties = db.get_all_properties()
        
        if all_properties:
            buy_count = len([p for p in all_properties if p.get('listing_type') == 'buy'])
            rent_count = len([p for p in all_properties if p.get('listing_type') == 'rent'])
            
            listing_data = pd.DataFrame({
                'Type': ['For Sale', 'For Rent'],
                'Count': [buy_count, rent_count]
            })
            
            fig_listing = px.bar(
                listing_data,
                x='Type',
                y='Count',
                color='Type',
                color_discrete_map={'For Sale': '#10b981', 'For Rent': '#f59e0b'}
            )
            fig_listing.update_layout(
                showlegend=False,
                height=300,
                margin=dict(l=20, r=20, t=30, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title="",
                yaxis_title="Properties"
            )
            st.plotly_chart(fig_listing, use_container_width=True)
        else:
            st.info("No listing data available for chart")
