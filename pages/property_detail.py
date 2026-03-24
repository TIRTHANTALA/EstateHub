"""
Property Detail Page for EstateHub
"""
import streamlit as st
from pages.components import render_navbar, render_property_card, render_footer
from database import db
from auth import is_logged_in, get_current_user, get_current_role
from utils.helpers import format_price, format_date, get_property_image_placeholder
from utils.recommendations import get_similar_properties

def render_property_detail():
    """Render property detail page"""
    render_navbar("Property")
    
    property_id = st.session_state.get("property_id")
    is_admin = is_logged_in() and get_current_role() == "admin"
    is_owner = is_logged_in() and get_current_role() == "owner"
    came_from_favorites = st.session_state.get("came_from_favorites", False)
    
    # Determine back navigation
    if is_admin:
        back_page = "admin_dashboard"
        back_label = "← Back to Admin Dashboard"
    elif is_owner and came_from_favorites:
        back_page = "owner_dashboard"
        back_label = "← Back to My Favorites"
    elif is_owner:
        back_page = "owner_dashboard"
        back_label = "← Back to Dashboard"
    else:
        back_page = "properties"
        back_label = "← Back to Properties"
    
    if not property_id:
        st.error("Property not found")
        if st.button(back_label):
            st.session_state.page = back_page
            st.rerun()
        return
    
    # Get property data
    property_data = db.get_property_by_id(property_id)
    if not property_data:
        st.error("Property not found")
        if st.button(back_label):
            st.session_state.page = back_page
            st.rerun()
        return
    
    # Increment views only on first page load (not on reruns)
    # Skip for admin
    if not is_admin:
        current_view_key = f"viewed_{property_id}"
        if current_view_key not in st.session_state:
            db.increment_views(property_id)
            st.session_state[current_view_key] = True
    
    # Back button
    if st.button(back_label):
        st.session_state.page = back_page
        # Clear navigation tracking
        if "came_from_favorites" in st.session_state:
            del st.session_state.came_from_favorites
        # Clear view tracking so next visit counts
        current_view_key = f"viewed_{property_id}"
        if current_view_key in st.session_state:
            del st.session_state[current_view_key]
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Property images with carousel
        images = property_data.get("images", [])
        placeholder = get_property_image_placeholder(property_data.get('property_type', 'Flat'))
        
        # If no images array, use single image
        if not images:
            single_img = property_data.get("image")
            if single_img:
                images = [single_img]
            else:
                images = [placeholder]
        
        # Initialize image index in session state
        carousel_key = f"carousel_{property_id}"
        if carousel_key not in st.session_state:
            st.session_state[carousel_key] = 0
        
        total_images = len(images)
        
        # Reset index if it's out of bounds
        if st.session_state[carousel_key] >= total_images:
            st.session_state[carousel_key] = 0
        
        current_idx = st.session_state[carousel_key]
        
        # Navigation buttons and image counter
        nav_col1, nav_col2, nav_col3 = st.columns([1, 3, 1])
        
        with nav_col1:
            if st.button("◀ Prev", key="prev_img", use_container_width=True, disabled=(total_images <= 1)):
                st.session_state[carousel_key] = (current_idx - 1) % total_images
                st.rerun()
        
        with nav_col2:
            st.markdown(f"""
                <div style="text-align: center; padding: 8px; background: #f1f5f9; border-radius: 8px;">
                    <span style="font-weight: 600; color: #6366f1;">{current_idx + 1}</span> / {total_images} images
                </div>
            """, unsafe_allow_html=True)
        
        with nav_col3:
            if st.button("Next ▶", key="next_img", use_container_width=True, disabled=(total_images <= 1)):
                st.session_state[carousel_key] = (current_idx + 1) % total_images
                st.rerun()
        
        # Display current image
        current_image = images[current_idx]
        if current_image.startswith("data:image"):
            st.markdown(f"""
                <div style="border-radius: 16px; overflow: hidden; margin: 1rem 0; box-shadow: 0 4px 15px rgba(0,0,0,0.1); background: #f8fafc;">
                    <img src="{current_image}" style="width: 100%; max-height: 500px; object-fit: contain; border-radius: 16px; display: block;">
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="border-radius: 16px; overflow: hidden; margin: 1rem 0; box-shadow: 0 4px 15px rgba(0,0,0,0.1); background: #f8fafc;">
                    <img src="{current_image}" style="width: 100%; max-height: 500px; object-fit: contain; border-radius: 16px; display: block;"
                        onerror="this.src='{placeholder}'">
                </div>
            """, unsafe_allow_html=True)
        
        # Thumbnail gallery (clickable)
        if total_images > 1:
            st.markdown("**All Images:**")
            thumb_cols = st.columns(min(total_images, 6))
            for i, img in enumerate(images[:6]):
                with thumb_cols[i]:
                    border_color = "#6366f1" if i == current_idx else "#e2e8f0"
                    if st.button(f"📷 {i+1}", key=f"thumb_{i}", use_container_width=True):
                        st.session_state[carousel_key] = i
                        st.rerun()
        
        # Property info
        st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div>
                    <h1 style="font-size: 1.8rem; font-weight: 700; color: #1a1a2e; margin: 0;">
                        {property_data.get('title', 'Property')}
                    </h1>
                    <p style="color: #64748b; margin: 0.5rem 0;">
                        📍 {property_data.get('city', '')}
                    </p>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 2rem; font-weight: 700; color: #6366f1;">
                        {format_price(property_data.get('price', 0), property_data.get('listing_type', 'buy'))}
                    </div>
                    {"<span class='verified-badge'>✓ Verified</span>" if property_data.get('verified') else "<span class='pending-badge'>Pending Verification</span>"}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Key Features
        features_cols = st.columns(4)
        with features_cols[0]:
            st.markdown(f"""
                <div class="info-card">
                    <div style="font-size: 1.5rem;">🛏️</div>
                    <div style="font-weight: 600;">{property_data.get('bedrooms', 0)} Bedrooms</div>
                </div>
            """, unsafe_allow_html=True)
        with features_cols[1]:
            st.markdown(f"""
                <div class="info-card">
                    <div style="font-size: 1.5rem;">🚿</div>
                    <div style="font-weight: 600;">{property_data.get('bathrooms', 0)} Bathrooms</div>
                </div>
            """, unsafe_allow_html=True)
        with features_cols[2]:
            st.markdown(f"""
                <div class="info-card">
                    <div style="font-size: 1.5rem;">📐</div>
                    <div style="font-weight: 600;">{property_data.get('area', 0)} sq.ft</div>
                </div>
            """, unsafe_allow_html=True)
        with features_cols[3]:
            st.markdown(f"""
                <div class="info-card">
                    <div style="font-size: 1.5rem;">🏠</div>
                    <div style="font-weight: 600;">{property_data.get('property_type', 'Flat')}</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Location Details
        locality = property_data.get('locality', '')
        landmark = property_data.get('landmark', '')
        address = property_data.get('address', '')
        
        if locality or address:
            st.markdown("""
                <h3 style="font-size: 1.25rem; font-weight: 700; color: #1a1a2e; margin: 1.5rem 0 1rem;">
                    📍 Location Details
                </h3>
            """, unsafe_allow_html=True)
            
            location_items = []
            if locality:
                location_items.append(f"<div><span style='color: #64748b; font-size: 0.85rem;'>Locality</span><div style='font-weight: 600; color: #1a1a2e; margin-top: 4px;'>{locality}</div></div>")
            if address:
                location_items.append(f"<div><span style='color: #64748b; font-size: 0.85rem;'>Address</span><div style='font-weight: 600; color: #1a1a2e; margin-top: 4px;'>{address}</div></div>")
            if landmark:
                location_items.append(f"<div><span style='color: #64748b; font-size: 0.85rem;'>Landmark</span><div style='font-weight: 600; color: #1a1a2e; margin-top: 4px;'>{landmark}</div></div>")
            
            grid_content = "".join(location_items)
            
            st.markdown(f"""
                <div style="background: #f8fafc; padding: 1.25rem; border-radius: 12px; margin-bottom: 1.5rem;">
                    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">
                        {grid_content}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        # Property Overview - Row-wise Grid Layout
        st.markdown("""
            <h3 style="font-size: 1.25rem; font-weight: 700; color: #1a1a2e; margin: 1.5rem 0 1rem;">
                🏠 Property Overview
            </h3>
        """, unsafe_allow_html=True)
        
        overview_items = [
            ("Property Type", property_data.get('property_type', 'N/A')),
            ("Built-up Area", f"{property_data.get('area', 0)} sq.ft"),
            ("Carpet Area", f"{property_data.get('carpet_area', 0)} sq.ft" if property_data.get('carpet_area') else None),
            ("Furnishing", property_data.get('furnishing', 'N/A')),
            ("Facing", property_data.get('facing', None)),
            ("Floor", f"{property_data.get('property_floor', 'N/A')} of {property_data.get('total_floors', 'N/A')}" if property_data.get('property_floor') else None),
            ("Property Age", property_data.get('property_age', None)),
            ("Availability", property_data.get('availability', None)),
            ("Balconies", property_data.get('balconies', None)),
            ("Parking", property_data.get('parking', None)),
            ("Water Supply", property_data.get('water_supply', None)),
        ]
        
        # Filter out None values
        valid_items = [(label, value) for label, value in overview_items if value and value != "N/A" and value != "0 sq.ft" and value != "N/A of N/A"]
        
        # Build HTML for overview grid
        overview_html = ""
        for label, value in valid_items:
            overview_html += f'<div style="background: white; padding: 1rem; border-radius: 10px; border: 1px solid #e2e8f0; text-align: center;"><div style="color: #64748b; font-size: 0.8rem; margin-bottom: 4px;">{label}</div><div style="font-weight: 700; color: #1a1a2e; font-size: 1rem;">{value}</div></div>'
        
        st.markdown(f'<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 1.5rem;">{overview_html}</div>', unsafe_allow_html=True)
        
        # Price Breakdown (for rent)
        if property_data.get('listing_type') == 'rent':
            security = property_data.get('security_deposit', 0)
            maintenance = property_data.get('maintenance', 0)
            if security or maintenance:
                st.markdown("### 💰 Price Breakdown")
                st.markdown(f"""
                    <div style="background: #f0f1ff; padding: 1rem; border-radius: 12px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                            <span>Monthly Rent</span>
                            <strong>{format_price(property_data.get('price', 0), 'rent')}</strong>
                        </div>
                        {f"<div style='display: flex; justify-content: space-between; margin-bottom: 8px;'><span>Security Deposit</span><strong>₹{security:,}</strong></div>" if security else ""}
                        {f"<div style='display: flex; justify-content: space-between;'><span>Maintenance</span><strong>₹{maintenance:,}/month</strong></div>" if maintenance else ""}
                    </div>
                """, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
        
        # Price Negotiable Badge
        if property_data.get('price_negotiable'):
            st.markdown("""
                <div style="background: #dcfce7; color: #16a34a; padding: 8px 12px; border-radius: 8px; display: inline-block;">
                    ✓ Price Negotiable
                </div>
            """, unsafe_allow_html=True)
            st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Description
        st.markdown("""
            <h3 style="font-size: 1.25rem; font-weight: 700; color: #1a1a2e; margin: 1.5rem 0 1rem;">
                📝 Description
            </h3>
        """, unsafe_allow_html=True)
        st.markdown(f"""
            <div style="background: #f8fafc; padding: 1.25rem; border-radius: 12px; margin-bottom: 1.5rem;">
                <p style="color: #475569; line-height: 1.8; margin: 0; font-size: 0.95rem;">
                    {property_data.get('description', 'No description available.')}
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Amenities
        amenities = property_data.get("amenities", [])
        if amenities:
            st.markdown("""
                <h3 style="font-size: 1.25rem; font-weight: 700; color: #1a1a2e; margin: 1.5rem 0 1rem;">
                    ✨ Amenities
                </h3>
            """, unsafe_allow_html=True)
            
            # Display amenities using st.write to avoid HTML escaping issues
            amenities_container = st.container()
            with amenities_container:
                cols = st.columns(min(len(amenities), 4))
                for i, amenity in enumerate(amenities):
                    col_idx = i % len(cols) if len(amenities) >= 4 else i
                    with cols[col_idx]:
                        st.markdown(f"""
                            <div style="background: #f0f1ff; color: #6366f1; padding: 8px 16px; border-radius: 20px; font-size: 0.9rem; font-weight: 500; text-align: center; margin: 4px;">
                                ✓ {amenity}
                            </div>
                        """, unsafe_allow_html=True)
    
    with col2:
        # Owner contact card - all in one HTML block
        owner_id = property_data.get("owner_id")
        owner = db.get_user_by_id(owner_id) if owner_id else None
        
        if owner:
            st.markdown(f"""
                <div class="dashboard-card" style="padding: 1.5rem; border-radius: 12px; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 1rem;">
                    <h4 style="font-weight: 600; margin-bottom: 1rem; color: #1a1a2e;">Contact Owner</h4>
                    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                        <div style="width: 50px; height: 50px; border-radius: 50%; 
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            display: flex; align-items: center; justify-content: center;
                            color: white; font-weight: 600; font-size: 1.2rem;">
                            {owner.get('name', 'O')[0]}
                        </div>
                        <div>
                            <div style="font-weight: 600; color: #1a1a2e;">{owner.get('name', 'Owner')}</div>
                            <div style="color: #64748b; font-size: 0.85rem;">Property Owner</div>
                        </div>
                    </div>
                    <div style="background: #f8fafc; padding: 12px; border-radius: 8px;">
                        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                            <span style="font-size: 1.1rem;">📞</span>
                            <span style="font-weight: 500; color: #1a1a2e;">{owner.get('phone', 'Not available')}</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="font-size: 1.1rem;">📧</span>
                            <span style="font-weight: 500; font-size: 0.9rem; color: #1a1a2e;">{owner.get('email', 'Not available')}</span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="dashboard-card" style="padding: 1.5rem; border-radius: 12px; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 1rem;">
                    <h4 style="font-weight: 600; margin-bottom: 1rem; color: #1a1a2e;">Contact Owner</h4>
                    <p style="color: #64748b;">Owner information not available</p>
                </div>
            """, unsafe_allow_html=True)
        
        # Actions
        if is_logged_in():
            user = get_current_user()
            user_id = str(user.get("_id", ""))
            
            # Check if current user owns this property
            current_user = get_current_user()
            is_owner_of_property = (current_user and 
                                   property_data.get("owner_id") == str(current_user.get("_id")))
            
            # Favorite button - available for all logged-in users except property owners
            if not is_owner_of_property:
                is_fav = db.is_favorite(user_id, property_id)
                if st.button("❤️ Remove from Favorites" if is_fav else "🤍 Add to Favorites", 
                            use_container_width=True):
                    if is_fav:
                        db.remove_favorite(user_id, property_id)
                        st.success("Removed from favorites!")
                        st.rerun()
                    else:
                        # Add favorite with user role
                        user_role = get_current_role()
                        db.add_favorite(user_id, property_id, user_role)
                        st.success("Added to favorites!")
                        st.rerun()
            else:
                st.info("This is your property - you cannot favorite your own listing")
            
            # Book visit - available for users and owners (for properties they don't own)
            if get_current_role() in ["user", "owner"] and not is_owner_of_property:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("### Schedule a Visit")
                
                from datetime import date
                visit_date = st.date_input("Preferred Date", min_value=date.today())
                visit_time = st.selectbox("Preferred Time", 
                    ["10:00 AM", "11:00 AM", "12:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM"])
                visit_message = st.text_area("Message to Owner *", 
                    placeholder="Any specific requirements?")
                
                if st.button("📅 Book Visit", type="primary", use_container_width=True):
                    if not visit_message or len(visit_message.strip()) < 5:
                        st.error("Please enter a message to the owner (at least 5 characters)")
                        st.stop()
                    visit_data = {
                        "user_id": user_id,
                        "owner_id": owner_id,
                        "property_id": property_id,
                        "property_title": property_data.get("title", ""),
                        "visit_date": str(visit_date),
                        "visit_time": visit_time,
                        "message": visit_message,
                        "user_name": user.get("name", ""),
                        "user_phone": user.get("phone", "")
                    }
                    db.create_visit(visit_data)
                    st.success("Visit request sent! The owner will contact you soon.")
        else:
            st.info("Please login to book a visit or save to favorites")
            if st.button("Login to Continue", use_container_width=True, type="primary"):
                st.session_state.page = "login"
                st.rerun()
        
        # Property details card - Better styled
        st.markdown("<br>", unsafe_allow_html=True)
        
        prop_id = str(property_data.get("_id", ""))[:10] + "..."
        listed_date = format_date(property_data.get("created_at"))
        listing_type = property_data.get("listing_type", "buy").capitalize()
        furnishing = property_data.get("furnishing", "Unfurnished")
        views = property_data.get('views', 0)
        
        st.markdown(f"""
            <div style="background: white; padding: 1.25rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                <h4 style="font-weight: 700; margin-bottom: 1rem; color: #1a1a2e; font-size: 1.1rem;">📋 Property Details</h4>
                <div style="display: flex; justify-content: space-between; padding: 0.75rem 0; border-bottom: 1px solid #f1f5f9;">
                    <span style="color: #64748b; font-size: 0.9rem;">Property ID</span>
                    <span style="font-weight: 600; color: #1a1a2e;">{prop_id}</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.75rem 0; border-bottom: 1px solid #f1f5f9;">
                    <span style="color: #64748b; font-size: 0.9rem;">Listed</span>
                    <span style="font-weight: 600; color: #1a1a2e;">{listed_date}</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.75rem 0; border-bottom: 1px solid #f1f5f9;">
                    <span style="color: #64748b; font-size: 0.9rem;">Listing Type</span>
                    <span style="font-weight: 600; color: #6366f1;">{listing_type}</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.75rem 0; border-bottom: 1px solid #f1f5f9;">
                    <span style="color: #64748b; font-size: 0.9rem;">Furnishing</span>
                    <span style="font-weight: 600; color: #1a1a2e;">{furnishing}</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.75rem 0;">
                    <span style="color: #64748b; font-size: 0.9rem;">Views</span>
                    <span style="font-weight: 600; color: #10b981;">{views} views</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Similar Properties (hide for admin)
    if not is_admin:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Similar Properties")
        
        similar = get_similar_properties(property_id)
        if similar:
            cols = st.columns(4)
            for i, prop in enumerate(similar[:4]):
                with cols[i]:
                    render_property_card(prop)
        else:
            st.info("No similar properties found")
        
        render_footer()
