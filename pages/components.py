"""
Reusable UI Components for EstateHub
"""
import streamlit as st
from utils.helpers import format_price, time_ago, get_property_image_placeholder

def render_navbar(current_page: str = "Home"):
    """Render navigation bar"""
    from auth import is_logged_in, get_current_user, get_current_role
    
    # Check if admin - show simplified navbar
    if is_logged_in() and get_current_role() == "admin":
        col1, col2, col3 = st.columns([2, 4, 2])
        
        with col1:
            st.markdown('<span class="logo-text">🏠 EstateHub</span>', unsafe_allow_html=True)
        
        with col2:
            pass  # Empty center for admin
        
        with col3:
            btn_cols = st.columns(2)
            user = get_current_user()
            with btn_cols[0]:
                st.markdown(f"""
                    <div style="display: flex; align-items: center; justify-content: center; 
                        padding: 0.5rem; background: #f0f1ff; border-radius: 8px; color: #6366f1; font-weight: 600;">
                        👤 {user.get('name', 'Admin')[:10]}
                    </div>
                """, unsafe_allow_html=True)
            with btn_cols[1]:
                if st.button("Logout", use_container_width=True):
                    from auth import clear_session
                    clear_session()
                    st.session_state.page = "home"
                    st.rerun()
        return
    
    # Regular navbar for non-admin users
    col1, col2, col3 = st.columns([2, 4, 2])
    
    with col1:
        st.markdown('<span class="logo-text">🏠 EstateHub</span>', unsafe_allow_html=True)
    
    with col2:
        nav_cols = st.columns(4)
        pages = ["Home", "Properties", "About", "Contact"]
        for i, page in enumerate(pages):
            with nav_cols[i]:
                if st.button(page, key=f"nav_{page}", use_container_width=True):
                    st.session_state.page = page.lower()
                    st.rerun()
    
    with col3:
        btn_cols = st.columns(2)
        
        if is_logged_in():
            user = get_current_user()
            role = get_current_role()
            with btn_cols[0]:
                if st.button(f"👤 {user.get('name', 'User')[:10]}", use_container_width=True):
                    st.session_state.page = "dashboard"
                    st.rerun()
            with btn_cols[1]:
                if st.button("Logout", use_container_width=True):
                    from auth import clear_session
                    clear_session()
                    st.session_state.page = "home"
                    st.rerun()
        else:
            with btn_cols[0]:
                if st.button("Login", use_container_width=True):
                    st.session_state.page = "login"
                    st.rerun()
            with btn_cols[1]:
                if st.button("Sign Up", use_container_width=True, type="primary"):
                    st.session_state.page = "register"
                    st.rerun()

def render_hero_section():
    """Render hero section matching reference UI"""
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown("""
            <div style="padding: 2rem 0;">
                <span style="background: #ede9fe; color: #6366f1; padding: 0.5rem 1rem; 
                    border-radius: 20px; font-size: 0.85rem; font-weight: 500;">
                    #1 Real Estate Platform
                </span>
                <h1 style="font-size: 3rem; font-weight: 700; color: #1a1a2e; 
                    line-height: 1.2; margin: 1.5rem 0 1rem;">
                    Find Your <span style="color: #6366f1;">Dream Home</span><br>With Ease
                </h1>
                <p style="color: #64748b; font-size: 1.1rem; margin-bottom: 2rem;">
                    Discover thousands of verified properties for buying and renting.
                    Your perfect home is just a click away.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        btn_col1, btn_col2, _ = st.columns([2, 2, 1])
        with btn_col1:
            if st.button("🏠 Buy Property", type="primary", use_container_width=True):
                st.session_state.page = "properties"
                st.session_state.listing_filter = "buy"
                st.rerun()
        with btn_col2:
            if st.button("🔑 Rent Property", use_container_width=True):
                st.session_state.page = "properties"
                st.session_state.listing_filter = "rent"
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        from database import db
        stats = db.get_analytics()
        stat_cols = st.columns(3)
        with stat_cols[0]:
            st.markdown(f"""
                <div class="stat-box">
                    <div class="stat-number">{stats.get('total_properties', 0)}+</div>
                    <div class="stat-label">Properties</div>
                </div>
            """, unsafe_allow_html=True)
        with stat_cols[1]:
            st.markdown(f"""
                <div class="stat-box">
                    <div class="stat-number">{stats.get('total_users', 0)}+</div>
                    <div class="stat-label">Happy Clients</div>
                </div>
            """, unsafe_allow_html=True)
        with stat_cols[2]:
            st.markdown("""
                <div class="stat-box">
                    <div class="stat-number">50+</div>
                    <div class="stat-label">Cities</div>
                </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <br></br> 
            <div style="background: linear-gradient(135deg, #818cf8 0%, #a78bfa 100%);
                border-radius: 20px; padding: 3rem; text-align: center; position: relative;
                min-height: 300px; display: flex; align-items: center; justify-content: center;">
                <div style="font-size: 5rem;">🏢</div>
                <div style="position: absolute; bottom: -20px; left: 50%; transform: translateX(-50%);
                    background: white; padding: 0.75rem 1.5rem; border-radius: 12px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); display: flex; align-items: center; gap: 0.5rem;">
                    <span style="color: #10b981;">✓</span>
                    <span><strong>Verified</strong><br><small style="color: #64748b;">500+ Properties</small></span>
                </div>
                <div style="position: absolute; top: 20px; right: 20px;
                    background: white; padding: 0.5rem 1rem; border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <span style="color: #fbbf24;">⭐</span>
                    <span style="font-weight: 600;">Rating</span><br>
                    <span style="font-weight: 700;">4.9/5</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

def render_search_box():
    """Render search/filter box"""
    st.markdown("<br></br>",unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🏠 Buy", "🔑 Rent"])
        
    import config
    
    with tab1:
        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
        with col1:
            city = st.selectbox("Location", ["All Cities"] + config.CITIES, key="buy_city")
        with col2:
            prop_type = st.selectbox("Property Type", ["All Types"] + config.PROPERTY_TYPES, key="buy_type")
        with col3:
            budget = st.selectbox("Budget", list(config.BUDGET_RANGES.keys()), key="buy_budget")
        with col4:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔍 Search", type="primary", use_container_width=True, key="buy_search"):
                st.session_state.page = "properties"
                st.session_state.search_filters = {
                    "city": city, "property_type": prop_type, 
                    "budget": budget, "listing_type": "buy"
                }
                st.rerun()
    
    with tab2:
        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
        with col1:
            city = st.selectbox("Location", ["All Cities"] + config.CITIES, key="rent_city")
        with col2:
            prop_type = st.selectbox("Property Type", ["All Types"] + config.PROPERTY_TYPES, key="rent_type")
        with col3:
            budget = st.selectbox("Budget", list(config.RENT_BUDGET_RANGES.keys()), key="rent_budget")
        with col4:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔍 Search", type="primary", use_container_width=True, key="rent_search"):
                st.session_state.page = "properties"
                st.session_state.search_filters = {
                    "city": city, "property_type": prop_type,
                    "budget": budget, "listing_type": "rent"
                }
                st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_property_card(property_data: dict, show_actions: bool = True):
    """Render a property card"""
    prop_id = str(property_data.get("_id", ""))
    title = property_data.get("title", "Property")
    price = property_data.get("price", 0)
    listing_type = property_data.get("listing_type", "buy")
    city = property_data.get("city", "")
    prop_type = property_data.get("property_type", "Flat")
    bedrooms = property_data.get("bedrooms", 0)
    area = property_data.get("area", 0)
    verified = property_data.get("verified", False)
    image = property_data.get("image") or get_property_image_placeholder(prop_type)
    
    with st.container():
        st.markdown(f"""
            <div class="property-card">
                <img src="{image}" class="property-image" alt="{title}"
                    onerror="this.src='{get_property_image_placeholder(prop_type)}'">
                <div class="property-content">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span class="property-price">{format_price(price, listing_type)}</span>
                        {"<span class='verified-badge'>✓ Verified</span>" if verified else ""}
                    </div>
                    <h3 class="property-title">{title[:40]}{'...' if len(title) > 40 else ''}</h3>
                    <p class="property-location">📍 {city}</p>
                    <div class="property-features">
                        <span class="feature-item">🛏️ {bedrooms} Beds</span>
                        <span class="feature-item">📐 {area} sq.ft</span>
                        <span class="feature-item">🏠 {prop_type}</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if show_actions:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("View Details", key=f"view_{prop_id}", use_container_width=True):
                    st.session_state.page = "property_detail"
                    st.session_state.property_id = prop_id
                    st.rerun()
            
            with col2:
                from auth import is_logged_in, get_current_user, get_current_role
                if is_logged_in():
                    from database import db
                    user = get_current_user()
                    user_id = str(user.get("_id", ""))
                    user_role = get_current_role()
                    
                    # Check if user owns this property
                    is_owner_of_property = (property_data.get("owner_id") == user_id)
                    
                    # Show favorite button only if not property owner
                    if not is_owner_of_property:
                        is_fav = db.is_favorite(user_id, prop_id)
                        if st.button("❤️" if is_fav else "🤍", key=f"fav_{prop_id}", use_container_width=True):
                            if is_fav:
                                db.remove_favorite(user_id, prop_id)
                            else:
                                db.add_favorite(user_id, prop_id, user_role)
                            st.rerun()
                    else:
                        # Show "My Property" indicator for owners
                        st.markdown("""
                            <div style="text-align: center; padding: 0.5rem; background: #f1f5f9; border-radius: 6px; font-size: 0.8rem; color: #64748b;">
                                🏠 My Property
                            </div>
                        """, unsafe_allow_html=True)

def render_feature_cards():
    """Render Why Choose Us feature cards"""
    st.markdown("""
        <div style="text-align: center; margin: 3rem 0 2rem;">
            <h2 style="font-size: 2rem; font-weight: 700; color: #1a1a2e;">
                Why Choose EstateHub?
            </h2>
            <p style="color: #64748b;">We make property search simple and trustworthy</p>
        </div>
    """, unsafe_allow_html=True)
    
    features = [
        {"icon": "✓", "title": "Verified Properties", 
         "desc": "All listings are verified by our team for authenticity and accuracy"},
        {"icon": "📍", "title": "Wide Coverage",
         "desc": "Properties across major cities in India with detailed locality info"},
        {"icon": "🎧", "title": "Expert Support",
         "desc": "Dedicated support team to help you throughout your journey"},
        {"icon": "⚡", "title": "Quick Process",
         "desc": "Streamlined process from search to property visit booking"}
    ]
    
    cols = st.columns(4)
    for i, feature in enumerate(features):
        with cols[i]:
            st.markdown(f"""
                <div class="info-card">
                    <div class="info-card-icon" style="background: #f0f1ff; color: #6366f1;">
                        {feature['icon']}
                    </div>
                    <h4 class="info-card-title">{feature['title']}</h4>
                    <p class="info-card-text">{feature['desc']}</p>
                </div>
            """, unsafe_allow_html=True)

def render_cta_section():
    """Render Call to Action section for property owners"""
    st.markdown("""
        <div class="cta-section">
            <h2 class="cta-title">Are You a Property Owner?</h2>
            <p class="cta-subtitle">
                List your property and reach thousands of potential buyers and tenants
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    _, col, _ = st.columns([1, 1, 1])
    with col:
        from auth import is_logged_in, get_current_role
        if is_logged_in() and get_current_role() == "owner":
            if st.button("📝 Add New Property", use_container_width=True):
                st.session_state.page = "add_property"
                st.rerun()
        else:
            if st.button("List Your Property →", use_container_width=True):
                st.session_state.page = "register"
                st.session_state.register_as = "owner"
                st.rerun()

def render_testimonials():
    """Render testimonials section"""
    st.markdown("""
        <div style="margin: 3rem 0;">
            <h2 style="font-size: 1.8rem; font-weight: 700; color: #1a1a2e; margin-bottom: 0.5rem;">
                Trusted by Thousands
            </h2>
            <p style="color: #64748b; margin-bottom: 2rem;">
                EstateHub has helped thousands of people find their perfect property.
                Our transparent process and verified listings make property search hassle-free.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        stat_cols = st.columns(2)
        with stat_cols[0]:
            st.markdown("""
                <div style="display: flex; align-items: center; gap: 1rem; padding: 1rem;">
                    <div style="background: #f0fdf4; padding: 1rem; border-radius: 12px;">🏠</div>
                    <div>
                        <div style="font-size: 1.8rem; font-weight: 700; color: #1a1a2e;">100+</div>
                        <div style="color: #64748b; font-size: 0.9rem;">Properties Sold</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        with stat_cols[1]:
            st.markdown("""
                <div style="display: flex; align-items: center; gap: 1rem; padding: 1rem;">
                    <div style="background: #fef3c7; padding: 1rem; border-radius: 12px;">👥</div>
                    <div>
                        <div style="font-size: 1.8rem; font-weight: 700; color: #1a1a2e;">50+</div>
                        <div style="color: #64748b; font-size: 0.9rem;">Happy Customers</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    testimonials = [
        {"text": "Found my dream apartment within a week. Excellent service!", 
         "author": "Rahul K.", "city": "Mumbai", "rating": 5},
        {"text": "Very professional owners and transparent process.",
         "author": "Priya S.", "city": "Bangalore", "rating": 5}
    ]
    
    with col2:
        test_cols = st.columns(2)
        for i, t in enumerate(testimonials):
            with test_cols[i]:
                st.markdown(f"""
                    <div class="testimonial-card">
                        <div class="testimonial-stars">{'⭐' * t['rating']}</div>
                        <p class="testimonial-text">"{t['text']}"</p>
                        <div class="testimonial-author">
                            <div class="testimonial-avatar">{t['author'][0]}</div>
                            <div>
                                <div style="font-weight: 600;">{t['author']}</div>
                                <div style="color: #64748b; font-size: 0.85rem;">{t['city']}</div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    
    st.markdown("<br></br>", unsafe_allow_html=True)

def render_footer():
    """Render footer section"""
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div>
                <div style="font-size: 1.3rem; font-weight: 700; color: #6366f1; margin-bottom: 1rem;">
                    🏠 EstateHub
                </div>
                <p style="color: #64748b; font-size: 0.9rem;">
                    Find your perfect home with our verified property listings.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div>
                <h4 style="font-weight: 600; margin-bottom: 0.75rem;">Quick Links</h4>
                <p style="color: #64748b; font-size: 0.9rem; margin: 0.3rem 0;">Buy Property</p>
                <p style="color: #64748b; font-size: 0.9rem; margin: 0.3rem 0;">Rent Property</p>
                <p style="color: #64748b; font-size: 0.9rem; margin: 0.3rem 0;">About Us</p>
                <p style="color: #64748b; font-size: 0.9rem; margin: 0.3rem 0;">Contact</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div>
                <h4 style="font-weight: 600; margin-bottom: 0.75rem;">Legal</h4>
                <p style="color: #64748b; font-size: 0.9rem; margin: 0.3rem 0;">Privacy Policy</p>
                <p style="color: #64748b; font-size: 0.9rem; margin: 0.3rem 0;">Terms of Service</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div>
                <h4 style="font-weight: 600; margin-bottom: 0.75rem;">Contact Us</h4>
                <p style="color: #64748b; font-size: 0.9rem; margin: 0.3rem 0;">📍 Ahmedabad, Gujarat, India</p>
                <p style="color: #64748b; font-size: 0.9rem; margin: 0.3rem 0;">✉️ estatehub32@gmail.com</p>
                <p style="color: #64748b; font-size: 0.9rem; margin: 0.3rem 0;">📞 +91 7984087441</p>
                <div style="margin-top: 0.5rem;">
                    <span style="background: #6366f1; color: white; padding: 0.2rem 0.5rem;
                        border-radius: 4px; font-size: 0.75rem;">Verified</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0 1rem; color: #64748b; font-size: 0.85rem;">
            © 2026 EstateHub. All rights reserved. Made with ❤️ in India
        </div>
    """, unsafe_allow_html=True)
