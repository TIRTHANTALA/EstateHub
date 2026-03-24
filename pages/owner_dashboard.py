"""
Owner Dashboard for EstateHub
"""
import streamlit as st
from pages.components import render_navbar, render_footer
from database import db
from auth import get_current_user, require_login, require_role
from utils.helpers import format_price, format_date, time_ago, get_property_image_placeholder, process_multiple_images, get_image_html
from utils.recommendations import suggest_price
import config

def render_owner_dashboard():
    """Render property owner dashboard"""
    render_navbar("Dashboard")
    require_login()
    
    user = get_current_user()
    user_id = str(user.get("_id", ""))
    
    st.markdown(f"""
        <div style="margin-bottom: 2rem;">
            <h1 style="font-size: 2rem; font-weight: 700; color: #1a1a2e;">
                Owner Dashboard 🏠
            </h1>
            <p style="color: #64748b;">Manage your property listings and visit requests</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Get owner data
    properties = db.get_properties_by_owner(user_id)
    visits = db.get_visits_for_owner(user_id)
    pending_visits = [v for v in visits if v.get("status") == "pending"]
    
    # Get owner's visit requests as buyer
    my_visit_requests = db.get_visits_by_user_with_details(user_id)
    owner_favorites = db.get_user_favorites_with_role(user_id)
    
    # Stats
    stat_cols = st.columns(4)
    
    stats = [
        ("🏠", "My Properties", len(properties)),
        ("✅", "Verified", len([p for p in properties if p.get("verified")])),
        ("📅", "Visit Requests", len(visits)),
        ("❤️", "My Favorites", len(owner_favorites))
    ]
    
    for i, (icon, label, value) in enumerate(stats):
        with stat_cols[i]:
            st.markdown(f"""
                <div class="dashboard-stat">
                    <div style="display: flex; align-items: center; gap: 0.75rem;">
                        <span style="font-size: 1.5rem;">{icon}</span>
                        <div>
                            <div class="dashboard-stat-number">{value}</div>
                            <div class="dashboard-stat-label">{label}</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Check if user is coming back from property details via favorites
    came_from_favorites = st.session_state.get("came_from_favorites", False)
    
    # Clear the navigation tracking after using it
    if came_from_favorites and "came_from_favorites" in st.session_state:
        del st.session_state.came_from_favorites
        # Set session state to show favorites tab
        st.session_state.show_favorites_tab = True
    
    # Check if we should show favorites tab directly
    show_favorites = st.session_state.get("show_favorites_tab", False)
    
    if show_favorites:
        # Clear the flag after using it
        del st.session_state.show_favorites_tab
        
        # Show favorites directly with tab interface
        st.markdown("""
            <div style="margin-bottom: 1.5rem;">
                <h2 style="font-size: 1.8rem; font-weight: 700; color: #1a1a2e; margin: 0;">
                    ❤️ My Favorite Properties
                </h2>
                <p style="color: #64748b; margin: 0.25rem 0 0;">Properties you've saved for reference</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Show tab navigation
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🏠 My Properties", "➕ Add Property", "📅 Visit Requests", "❤️ My Favorites", "📋 My Visit Requests", "👤 Profile"])
        
        # Automatically show favorites tab content
        with tab4:
            render_owner_favorites(owner_favorites)
        
        # Other tabs (empty but visible for navigation)
        with tab1:
            st.info("Click 'My Properties' tab to view your properties")
        with tab2:
            st.info("Click 'Add Property' tab to add new properties")
        with tab3:
            st.info("Click 'Visit Requests' tab to view visit requests")
        with tab5:
            st.info("Click 'My Visit Requests' tab to view your visit requests")
        with tab6:
            st.info("Click 'Profile' tab to view your profile")
        
        render_footer()
        return
    
    # Normal dashboard tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🏠 My Properties", "➕ Add Property", "📅 Visit Requests", "❤️ My Favorites", "📋 My Visit Requests", "👤 Profile"])
    
    with tab1:
        render_owner_properties(properties, user_id)
    
    with tab2:
        render_add_property_form(user_id)
    
    with tab3:
        render_visit_requests(visits)
    
    with tab4:
        render_owner_favorites(owner_favorites)
    
    with tab5:
        render_my_visit_requests(my_visit_requests)
    
    with tab6:
        from pages.dashboard import render_profile_section
        render_profile_section(user)
    
    render_footer()

def render_owner_properties(properties: list, user_id: str):
    """Render owner's property listings"""
    if not properties:
        st.info("You haven't listed any properties yet. Click 'Add Property' to get started!")
        return
    
    for prop in properties:
        prop_id = str(prop.get("_id", ""))
        verified = prop.get("verified", False)
        
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            image = prop.get("image") or get_property_image_placeholder(prop.get("property_type", "Flat"))
            st.markdown(f"""
                <div class="dashboard-card" style="display: flex; gap: 1rem;">
                    <img src="{image}" style="width: 120px; height: 90px; border-radius: 10px; object-fit: cover;"
                        onerror="this.src='{get_property_image_placeholder(prop.get('property_type', 'Flat'))}'">
                    <div>
                        <h4 style="font-weight: 600; margin: 0;">{prop.get('title', 'Property')}</h4>
                        <p style="color: #64748b; margin: 0.25rem 0;">📍 {prop.get('city', '')}</p>
                        <div style="display: flex; gap: 1rem; align-items: center;">
                            <span style="font-weight: 600; color: #6366f1;">
                                {format_price(prop.get('price', 0), prop.get('listing_type', 'buy'))}
                            </span>
                            {"<span class='verified-badge'>✓ Verified</span>" if verified else "<span class='pending-badge'>⏳ Pending</span>"}
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button("✏️ Edit", key=f"edit_{prop_id}", use_container_width=True):
                st.session_state.edit_property_id = prop_id
                st.session_state.page = "edit_property"
                st.rerun()
        
        with col3:
            if st.button("🗑️ Delete", key=f"del_{prop_id}", use_container_width=True):
                if db.delete_property(prop_id):
                    st.success("Property deleted")
                    st.rerun()

def render_add_property_form(user_id: str):
    """Render add property form with detailed fields like 99acres"""
    # Get form key for resetting form fields
    form_key = st.session_state.get("add_property_form_key", 0)
    
    st.markdown("""
        <h2 style="font-size: 1.75rem; font-weight: 700; color: #1a1a2e; margin-bottom: 1.5rem;">
            📝 List a New Property
        </h2>
    """, unsafe_allow_html=True)
    
    # ===== SECTION 1: BASIC DETAILS =====
    st.markdown("""
        <h3 style="font-size: 1.1rem; font-weight: 600; color: #1a1a2e; margin: 1.5rem 0 1rem; 
            padding-bottom: 0.5rem; border-bottom: 2px solid #6366f1;">
            📋 Basic Details
        </h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        listing_type = st.radio("You're looking to... *", ["buy", "rent"], 
                                format_func=lambda x: "Sell" if x == "buy" else "Rent / Lease", 
                                horizontal=True, key=f"add_listing_type_{form_key}")
        property_type = st.selectbox("Property Type *", config.PROPERTY_TYPES, key=f"property_type_{form_key}")
    
    with col2:
        title = st.text_input("Property Title *", placeholder="e.g., Modern 3BHK Apartment in Prime Location", key=f"title_{form_key}")
        availability = st.selectbox("Availability Status", config.AVAILABILITY_STATUS, key=f"availability_{form_key}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ===== SECTION 2: LOCATION DETAILS =====
    st.markdown("""
        <h3 style="font-size: 1.1rem; font-weight: 600; color: #1a1a2e; margin: 1.5rem 0 1rem; 
            padding-bottom: 0.5rem; border-bottom: 2px solid #6366f1;">
            📍 Location Details
        </h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        city = st.selectbox("City *", config.CITIES, key=f"city_{form_key}")
        locality = st.text_input("Locality / Area *", placeholder="e.g., Andheri West, Koramangala", key=f"locality_{form_key}")
        landmark = st.text_input("Landmark", placeholder="Near Metro Station, Hospital, etc.", key=f"landmark_{form_key}")
    
    with col2:
        address = st.text_area("Full Address", placeholder="Building name, Street, Area...", height=100, key=f"address_{form_key}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ===== SECTION 3: PROPERTY PROFILE =====
    st.markdown("""
        <h3 style="font-size: 1.1rem; font-weight: 600; color: #1a1a2e; margin: 1.5rem 0 1rem; 
            padding-bottom: 0.5rem; border-bottom: 2px solid #6366f1;">
            🏠 Property Profile
        </h3>
    """, unsafe_allow_html=True)
    
    # Area Details
    st.markdown("**Area Details**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        buildup_area = st.number_input("Built-up Area (sq.ft) *", min_value=100, max_value=50000, value=1000,
                                        help="Carpet area + walls + balcony", key=f"buildup_area_{form_key}")
    with col2:
        carpet_area = st.number_input("Carpet Area (sq.ft)", min_value=0, max_value=50000, value=0, 
                                       help="Actual usable floor area", key=f"carpet_area_{form_key}")
    with col3:
        super_buildup = st.number_input("Super Built-up Area (sq.ft)", min_value=0, max_value=50000, value=0,
                                         help="Built-up + common areas share", key=f"super_buildup_{form_key}")
    
    # Room Details
    st.markdown("**Room Details**")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        bedrooms = st.selectbox("Bedrooms *", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], index=1, key=f"bedrooms_{form_key}")
    with col2:
        bathrooms = st.selectbox("Bathrooms *", [1, 2, 3, 4, 5, 6], index=1, key=f"bathrooms_{form_key}")
    with col3:
        balconies = st.selectbox("Balconies", [0, 1, 2, 3, "3+"], index=1, key=f"balconies_{form_key}")
    with col4:
        parking = st.selectbox("Parking Spaces", [0, 1, 2, 3, "3+"], index=1, key=f"parking_{form_key}")
    
    # Floor Details
    st.markdown("**Floor & Other Details**")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_floors = st.number_input("Total Floors", min_value=1, max_value=100, value=10, key=f"total_floors_{form_key}")
    with col2:
        property_floor = st.selectbox("Property Floor", config.FLOOR_OPTIONS, key=f"property_floor_{form_key}")
    with col3:
        facing = st.selectbox("Facing", config.FACING_DIRECTIONS, key=f"facing_{form_key}")
    with col4:
        furnishing = st.selectbox("Furnishing", ["Unfurnished", "Semi-Furnished", "Fully Furnished"], key=f"furnishing_{form_key}")
    
    # Additional Details
    col1, col2, col3 = st.columns(3)
    
    with col1:
        property_age = st.selectbox("Property Age", config.PROPERTY_AGE, key=f"property_age_{form_key}")
    with col2:
        water_supply = st.selectbox("Water Supply", ["Corporation", "Borewell", "Both", "24 Hours"], key=f"water_supply_{form_key}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ===== SECTION 4: PRICING =====
    st.markdown("""
        <h3 style="font-size: 1.1rem; font-weight: 600; color: #1a1a2e; margin: 1.5rem 0 1rem; 
            padding-bottom: 0.5rem; border-bottom: 2px solid #6366f1;">
            💰 Price Details
        </h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        price = st.number_input(
            f"Expected Price * ({'₹/month' if listing_type == 'rent' else '₹'})",
            min_value=1000,
            value=5000000 if listing_type == "buy" else 25000,
            key=f"price_{form_key}"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        price_negotiable = st.checkbox("Price Negotiable", key=f"price_negotiable_{form_key}")
    
    if listing_type == "rent":
        col1, col2 = st.columns(2)
        with col1:
            security_deposit = st.number_input("Security Deposit (₹)", min_value=0, value=50000, key=f"security_deposit_{form_key}")
        with col2:
            maintenance = st.number_input("Maintenance (₹/month)", min_value=0, value=2000, key=f"maintenance_{form_key}")
    else:
        security_deposit = 0
        maintenance = 0
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ===== SECTION 5: DESCRIPTION =====
    st.markdown("""
        <h3 style="font-size: 1.1rem; font-weight: 600; color: #1a1a2e; margin: 1.5rem 0 1rem; 
            padding-bottom: 0.5rem; border-bottom: 2px solid #6366f1;">
            📝 Description
        </h3>
    """, unsafe_allow_html=True)
    description = st.text_area("Property Description *", placeholder="Describe your property in detail - location advantages, nearby facilities, special features...", height=120, key=f"description_{form_key}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ===== SECTION 6: AMENITIES =====
    st.markdown("""
        <h3 style="font-size: 1.1rem; font-weight: 600; color: #1a1a2e; margin: 1.5rem 0 1rem; 
            padding-bottom: 0.5rem; border-bottom: 2px solid #6366f1;">
            ✨ Amenities <span style="font-size: 0.8rem; color: #64748b; font-weight: 400;">(Select all that apply)</span>
        </h3>
    """, unsafe_allow_html=True)
    
    amenity_categories = {
        "🏊 Recreation": ["Swimming Pool", "Gym", "Club House", "Play Area", "Garden"],
        "🔒 Security": ["24x7 Security", "CCTV", "Gated Community", "Intercom"],
        "🚗 Convenience": ["Parking", "Lift", "Power Backup", "Gas Pipeline", "Water Storage"],
        "🏢 Building": ["Maintenance Staff", "Fire Safety", "Rain Water Harvesting"]
    }
    
    all_amenities = []
    cols = st.columns(len(amenity_categories))
    for i, (category, options) in enumerate(amenity_categories.items()):
        with cols[i]:
            st.markdown(f"<p style='font-weight: 600; font-size: 0.9rem; margin-bottom: 8px;'>{category}</p>", unsafe_allow_html=True)
            for amenity in options:
                if st.checkbox(amenity, key=f"amenity_{amenity}_{form_key}"):
                    all_amenities.append(amenity)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ===== SECTION 7: IMAGES =====
    st.markdown("""
        <h3 style="font-size: 1.1rem; font-weight: 600; color: #1a1a2e; margin: 1.5rem 0 1rem; 
            padding-bottom: 0.5rem; border-bottom: 2px solid #6366f1;">
            📷 Property Images *
        </h3>
    """, unsafe_allow_html=True)
    st.caption("Minimum 2 images, Maximum 10 | Formats: JPG, PNG, AVIF")
    
    uploaded_images = st.file_uploader(
        "Upload Property Images",
        type=["jpg", "jpeg", "png", "avif"],
        accept_multiple_files=True,
        key=f"property_images_{form_key}"
    )
    
    if uploaded_images:
        if len(uploaded_images) > 10:
            st.warning("Maximum 10 images allowed. Only first 10 will be used.")
            uploaded_images = uploaded_images[:10]
        
        if len(uploaded_images) < 2:
            st.warning("Please upload at least 2 images.")
        
        color = "#10b981" if len(uploaded_images) >= 2 else "#f59e0b"
        bg_color = "#f0fdf4" if len(uploaded_images) >= 2 else "#fef3c7"
        st.markdown(f"""
            <div style="background: {bg_color}; border: 1px solid {color}; border-radius: 8px; padding: 12px; margin-top: 10px;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                    <span style="color: {color}; font-size: 18px;">{"✓" if len(uploaded_images) >= 2 else "⚠"}</span>
                    <strong style="color: #1a1a2e;">{len(uploaded_images)} image(s) selected</strong>
                </div>
                <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                    {"".join([f'<span style="background: white; color: #1a1a2e; padding: 4px 10px; border-radius: 15px; font-size: 12px; border: 1px solid #e2e8f0;">📷 {img.name[:20]}{"..." if len(img.name) > 20 else ""}</span>' for img in uploaded_images])}
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ===== SUBMIT =====
    if st.button("📝 List Property", type="primary", use_container_width=True):
        if not title or len(title) < 5:
            st.error("Please enter a valid property title (minimum 5 characters)")
        elif not locality:
            st.error("Please enter the locality/area")
        elif not description or len(description) < 20:
            st.error("Please provide a detailed description (at least 20 characters)")
        elif not uploaded_images or len(uploaded_images) < 2:
            st.error("Please upload at least 2 images")
        else:
            images = process_multiple_images(uploaded_images) if uploaded_images else []
            
            property_data = {
                "title": title,
                "property_type": property_type,
                "listing_type": listing_type,
                "availability": availability,
                # Location
                "city": city,
                "locality": locality,
                "address": address,
                "landmark": landmark,
                # Area
                "carpet_area": carpet_area,
                "area": buildup_area,
                "super_buildup_area": super_buildup,
                # Room details
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "balconies": balconies if isinstance(balconies, int) else 4,
                "parking": parking if isinstance(parking, int) else 4,
                # Floor details
                "total_floors": total_floors,
                "property_floor": property_floor,
                "facing": facing,
                # Additional
                "property_age": property_age,
                "furnishing": furnishing,
                "water_supply": water_supply,
                # Pricing
                "price": price,
                "price_negotiable": price_negotiable,
                "security_deposit": security_deposit,
                "maintenance": maintenance,
                # Others
                "description": description,
                "amenities": all_amenities,
                "images": images,
                "image": images[0] if images else None,
                "owner_id": user_id
            }
            
            prop_id = db.create_property(property_data)
            if prop_id:
                st.success("🎉 Property listed successfully! It will be visible after admin verification.")
                st.balloons()
                # Clear all form fields by incrementing form key to reset the form
                if "add_property_form_key" not in st.session_state:
                    st.session_state.add_property_form_key = 0
                st.session_state.add_property_form_key += 1
                st.rerun()
            else:
                st.error("Failed to list property. Please try again.")

def render_visit_requests(visits: list):
    """Render visit requests for owner"""
    if not visits:
        st.info("No visit requests yet. Your properties will receive requests once they are verified.")
        return
    
    for visit in visits:
        visit_id = str(visit.get("_id", ""))
        status = visit.get("status", "pending")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            status_colors = {"pending": "#f59e0b", "approved": "#10b981", "rejected": "#ef4444"}
            st.markdown(f"""
                <div class="dashboard-card">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <h4 style="font-weight: 600; margin: 0;">
                                Visit Request for: {visit.get('property_title', 'Property')}
                            </h4>
                            <p style="color: #64748b; margin: 0.5rem 0;">
                                <strong>From:</strong> {visit.get('user_name', 'User')} | 📞 {visit.get('user_phone', '')}
                            </p>
                            <p style="color: #64748b; margin: 0;">
                                📅 Requested for: {visit.get('visit_date', '')} at {visit.get('visit_time', '')}
                            </p>
                            {f"<p style='margin-top: 0.5rem;'><em>{visit.get('message', '')}</em></p>" if visit.get('message') else ""}
                        </div>
                        <span style="background: {status_colors.get(status, '#64748b')};
                            color: white; padding: 0.25rem 0.75rem; border-radius: 20px;
                            font-size: 0.8rem; text-transform: capitalize;">
                            {status}
                        </span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if status == "pending":
                if st.button("✅ Approve", key=f"approve_{visit_id}", use_container_width=True):
                    db.update_visit_status(visit_id, "approved")
                    st.rerun()
                if st.button("❌ Reject", key=f"reject_{visit_id}", use_container_width=True):
                    db.update_visit_status(visit_id, "rejected")
                    st.rerun()

def render_edit_property():
    """Render edit property page"""
    render_navbar("Edit Property")
    require_login()
    
    property_id = st.session_state.get("edit_property_id")
    if not property_id:
        st.error("Property not found")
        if st.button("← Back to Dashboard"):
            st.session_state.page = "owner_dashboard"
            st.rerun()
        return
    
    # Get property data
    property_data = db.get_property_by_id(property_id)
    if not property_data:
        st.error("Property not found")
        if st.button("← Back to Dashboard"):
            st.session_state.page = "owner_dashboard"
            st.rerun()
        return
    
    user = get_current_user()
    user_id = str(user.get("_id", ""))
    
    # Verify ownership
    if property_data.get("owner_id") != user_id:
        st.error("You don't have permission to edit this property")
        if st.button("← Back to Dashboard"):
            st.session_state.page = "owner_dashboard"
            st.rerun()
        return
    
    st.markdown("""
        <h1 style="font-size: 2rem; font-weight: 700; color: #1a1a2e;">
            ✏️ Edit Property
        </h1>
    """, unsafe_allow_html=True)
    
    if st.button("← Back to Dashboard"):
        st.session_state.page = "owner_dashboard"
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        title = st.text_input("Property Title", value=property_data.get("title", ""))
        property_type = st.selectbox("Property Type", config.PROPERTY_TYPES, 
                                     index=config.PROPERTY_TYPES.index(property_data.get("property_type", "Flat")))
        city = st.selectbox("City", config.CITIES,
                           index=config.CITIES.index(property_data.get("city", config.CITIES[0])))
        listing_type = st.radio("Listing Type", ["buy", "rent"], 
                               index=0 if property_data.get("listing_type") == "buy" else 1,
                               format_func=str.capitalize, horizontal=True)
    
    with col2:
        bedrooms = st.number_input("Bedrooms", min_value=1, max_value=10, 
                                   value=property_data.get("bedrooms", 2))
        bathrooms = st.number_input("Bathrooms", min_value=1, max_value=10,
                                    value=property_data.get("bathrooms", 2))
        area = st.number_input("Area (sq.ft)", min_value=100, max_value=50000,
                              value=property_data.get("area", 1000))
        furnishing = st.selectbox("Furnishing", ["Unfurnished", "Semi-Furnished", "Fully Furnished"],
                                  index=["Unfurnished", "Semi-Furnished", "Fully Furnished"].index(
                                      property_data.get("furnishing", "Unfurnished")))
    
    price = st.number_input(
        f"Price ({'₹/month' if listing_type == 'rent' else '₹'})",
        min_value=1000,
        value=property_data.get("price", 5000000)
    )
    
    description = st.text_area("Description", value=property_data.get("description", ""), height=150)
    
    # Amenities
    st.markdown("### Amenities")
    amenity_options = ["Parking", "Gym", "Swimming Pool", "Security", "Power Backup", 
                       "Lift", "Garden", "Club House", "Children's Play Area", "Gas Pipeline"]
    amenities = st.multiselect("Select Amenities", amenity_options, 
                               default=property_data.get("amenities", []))
    
    # Current images info - handle both 'images' array and single 'image' field
    current_images = property_data.get("images", [])
    if not current_images:
        single_image = property_data.get("image")
        if single_image:
            current_images = [single_image]
    
    if current_images:
        st.info(f"📷 Currently {len(current_images)} image(s) uploaded")
    
    # New image upload
    st.markdown("### Manage Images")
    st.caption("📷 Supported formats: JPG, PNG, AVIF")
    image_action = st.radio(
        "What would you like to do?",
        ["Keep current images", "Add more images", "Replace all images"],
        horizontal=True,
        key="image_action"
    )
    
    uploaded_images = None
    if image_action in ["Add more images", "Replace all images"]:
        uploaded_images = st.file_uploader(
            "Upload Property Images",
            type=["jpg", "jpeg", "png", "avif"],
            accept_multiple_files=True,
            key="edit_property_images"
        )
        
        if uploaded_images:
            if image_action == "Add more images":
                total_after = len(current_images) + len(uploaded_images)
                if total_after > 10:
                    st.warning(f"Maximum 10 images allowed. You can add {10 - len(current_images)} more.")
                    uploaded_images = uploaded_images[:10 - len(current_images)]
                st.success(f"✓ {len(uploaded_images)} new image(s) will be added to existing {len(current_images)}")
            else:
                if len(uploaded_images) > 10:
                    st.warning("Maximum 10 images allowed.")
                    uploaded_images = uploaded_images[:10]
                st.success(f"✓ {len(uploaded_images)} image(s) will replace current images")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save Changes", type="primary", use_container_width=True):
            if not title or len(title) < 5:
                st.error("Please enter a valid property title")
            elif not description or len(description) < 20:
                st.error("Please provide a detailed description (at least 20 characters)")
            else:
                # Process images based on action
                if image_action == "Keep current images":
                    images = current_images
                elif image_action == "Add more images" and uploaded_images:
                    new_images = process_multiple_images(uploaded_images)
                    images = current_images + new_images
                elif image_action == "Replace all images" and uploaded_images:
                    images = process_multiple_images(uploaded_images)
                else:
                    images = current_images
                
                update_data = {
                    "title": title,
                    "property_type": property_type,
                    "city": city,
                    "listing_type": listing_type,
                    "bedrooms": bedrooms,
                    "bathrooms": bathrooms,
                    "area": area,
                    "furnishing": furnishing,
                    "price": price,
                    "description": description,
                    "amenities": amenities,
                    "images": images,
                    "image": images[0] if images else None,
                    "verified": False  # Re-verification needed after edit
                }
                
                if db.update_property(property_id, update_data):
                    st.success("Property updated successfully! It will need re-verification.")
                    st.session_state.page = "owner_dashboard"
                    st.rerun()
                else:
                    st.error("Failed to update property. Please try again.")
    
    with col2:
        if st.button("Cancel", use_container_width=True):
            st.session_state.page = "owner_dashboard"
            st.rerun()
    
    render_footer()

def render_owner_favorites(favorites: list):
    """Render owner's favorited properties"""
    st.markdown("""
        <div style="margin-bottom: 1.5rem;">
            <h3 style="font-size: 1.5rem; font-weight: 600; color: #1a1a2e; margin: 0;">
                ❤️ My Favorite Properties
            </h3>
            <p style="color: #64748b; margin: 0.25rem 0 0;">Properties you've saved for reference</p>
        </div>
    """, unsafe_allow_html=True)
    
    if not favorites:
        st.info("You haven't favorited any properties yet. Browse properties and save your favorites!")
        return
    
    for prop in favorites:
        prop_id = str(prop.get("_id", ""))
        title = prop.get("title", "Property")
        price = prop.get("price", 0)
        listing_type = prop.get("listing_type", "buy")
        city = prop.get("city", "")
        bedrooms = prop.get("bedrooms", 0)
        area = prop.get("area", 0)
        image = prop.get("image", get_property_image_placeholder(prop.get("property_type", "Flat")))
        favorited_by_role = prop.get("favorited_by_role", "user")
        
        # Property card
        with st.container():
            st.markdown(f"""
                <div style="border: 1px solid #e2e8f0; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; background: white;">
                    <div style="display: flex; gap: 1rem;">
                        <div style="flex-shrink: 0;">
                            <img src="{image}" style="width: 150px; height: 100px; object-fit: cover; border-radius: 8px;">
                        </div>
                        <div style="flex-grow: 1;">
                            <div style="display: flex; justify-content: space-between; align-items: start;">
                                <div>
                                    <h4 style="margin: 0 0 0.25rem 0; color: #1a1a2e; font-weight: 600;">{title}</h4>
                                    <p style="margin: 0 0 0.5rem 0; color: #64748b; font-size: 0.9rem;">📍 {city}</p>
                                </div>
                                <div style="text-align: right;">
                                    <div style="font-size: 1.25rem; font-weight: 700; color: #6366f1;">
                                        {format_price(price, listing_type)}
                                    </div>
                                    <span style="font-size: 0.75rem; color: #94a3b8; background: #f1f5f9; padding: 2px 6px; border-radius: 4px;">
                                        Favorited as {favorited_by_role}
                                    </span>
                                </div>
                            </div>
                            <div style="display: flex; gap: 1rem; margin-bottom: 0.5rem;">
                                <span style="font-size: 0.85rem; color: #64748b;">🛏️ {bedrooms} Beds</span>
                                <span style="font-size: 0.85rem; color: #64748b;">📐 {area} sq.ft</span>
                            </div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Streamlit buttons for functionality
            st.markdown("""
                <style>
                div[data-testid="stHorizontalBlock"] > div:has(button[data-testid*="view_"]) > button {
                    background-color: #6366f1 !important;
                    color: white !important;
                    border: none !important;
                    font-weight: 500 !important;
                }
                div[data-testid="stHorizontalBlock"] > div:has(button[data-testid*="remove_"]) > button {
                    background-color: #ef4444 !important;
                    color: white !important;
                    border: none !important;
                    font-weight: 500 !important;
                }
                </style>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(f"👁️ View Details", key=f"view_{prop_id}", use_container_width=True):
                    st.session_state.property_id = prop_id
                    st.session_state.page = "property_detail"
                    st.session_state.came_from_favorites = True  # Track navigation source
                    st.rerun()
            
            with col2:
                if st.button(f"🗑️ Remove", key=f"remove_{prop_id}", use_container_width=True):
                    user = get_current_user()
                    user_id = str(user.get("_id", ""))
                    if db.remove_favorite(user_id, prop_id):
                        st.success("Removed from favorites!")
                        st.rerun()
                    else:
                        st.error("Failed to remove from favorites")

def render_my_visit_requests(visit_requests: list):
    """Render owner's visit requests as buyer"""
    st.markdown("""
        <div style="margin-bottom: 1.5rem;">
            <h3 style="font-size: 1.5rem; font-weight: 600; color: #1a1a2e; margin: 0;">
                📋 My Visit Requests
            </h3>
            <p style="color: #64748b; margin: 0.25rem 0 0;">Properties you've requested to visit</p>
        </div>
    """, unsafe_allow_html=True)
    
    if not visit_requests:
        st.info("You haven't requested any property visits yet. Browse properties and schedule visits!")
        return
    
    for visit in visit_requests:
        prop_details = visit.get("property_details", {})
        if not prop_details:
            continue
            
        prop_id = str(prop_details.get("_id", ""))
        title = prop_details.get("title", "Property")
        price = prop_details.get("price", 0)
        listing_type = prop_details.get("listing_type", "buy")
        city = prop_details.get("city", "")
        status = visit.get("status", "pending")
        visit_date = visit.get("visit_date", "")
        visit_time = visit.get("visit_time", "")
        message = visit.get("message", "")
        created_at = visit.get("created_at")
        
        # Status color coding
        status_colors = {
            "pending": "#f59e0b",
            "approved": "#10b981", 
            "rejected": "#ef4444"
        }
        status_color = status_colors.get(status, "#64748b")
        
        with st.container():
            # Header with title, city, price and status
            header_col1, header_col2 = st.columns([3, 1])
            with header_col1:
                st.markdown(f"**{title}**")
                st.caption(f"📍 {city}")
            with header_col2:
                st.markdown(f"**{format_price(price, listing_type)}**")
                st.markdown(f"<span style='font-size: 0.85rem; color: white; background: {status_color}; padding: 4px 8px; border-radius: 6px;'>{status.upper()}</span>", unsafe_allow_html=True)
            
            # Visit details
            detail_col1, detail_col2 = st.columns(2)
            with detail_col1:
                st.caption("📅 Scheduled Date")
                st.write(visit_date)
            with detail_col2:
                st.caption("🕐 Time")
                st.write(visit_time)
            
            if message:
                st.caption("💬 Message")
                st.write(message)
            
            st.caption(f"Requested {time_ago(created_at) if created_at else ''}")
            st.markdown("---")
            
            visit_id = str(visit.get("_id", ""))
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(f"👁️ View Property", key=f"view_visit_prop_{visit_id}", use_container_width=True):
                    st.session_state.property_id = prop_id
                    st.session_state.page = "property_detail"
                    st.rerun()
            
            with col2:
                if status == "pending":
                    if st.button(f"❌ Cancel Visit", key=f"cancel_visit_{visit_id}", use_container_width=True):
                        if db.update_visit_status(visit_id, "cancelled"):
                            st.success("Visit request cancelled!")
                            st.rerun()
                        else:
                            st.error("Failed to cancel visit request")
