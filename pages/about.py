"""
About Page for EstateHub
"""
import streamlit as st
from pages.components import render_navbar, render_footer

def render_about():
    """Render about page"""
    render_navbar("About")
    
    st.markdown("""
        <div style="text-align: center; padding: 3rem 0;">
            <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">
                About EstateHub
            </h1>
            <p style="color: #64748b; max-width: 600px; margin: 1rem auto;">
                Your trusted partner in finding the perfect property
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Mission Section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="dashboard-card" style="padding: 2rem;">
                <h2 style="color: #6366f1; margin-bottom: 1rem;">🎯 Our Mission</h2>
                <p style="color: #64748b; line-height: 1.8;">
                    At EstateHub, we believe finding your dream home should be simple, 
                    transparent, and stress-free. Our platform connects genuine property 
                    seekers with verified owners, ensuring a safe and efficient property 
                    search experience.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="dashboard-card" style="padding: 2rem;">
                <h2 style="color: #6366f1; margin-bottom: 1rem;">👁️ Our Vision</h2>
                <p style="color: #64748b; line-height: 1.8;">
                    To become India's most trusted real estate platform where every 
                    listing is verified, every transaction is transparent, and every 
                    user finds their perfect property match.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Values
    st.markdown("""
        <h2 style="text-align: center; margin: 2rem 0;">Our Core Values</h2>
    """, unsafe_allow_html=True)
    
    values = [
        {"icon": "🔒", "title": "Trust", "desc": "Every listing is verified for authenticity"},
        {"icon": "🎯", "title": "Transparency", "desc": "Clear pricing and honest information"},
        {"icon": "⚡", "title": "Efficiency", "desc": "Quick and easy property discovery"},
        {"icon": "🤝", "title": "Support", "desc": "Dedicated team to help you at every step"}
    ]
    
    cols = st.columns(4)
    for i, value in enumerate(values):
        with cols[i]:
            st.markdown(f"""
                <div style="text-align: center; padding: 1.5rem;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">{value['icon']}</div>
                    <h3 style="color: #1a1a2e; font-weight: 600;">{value['title']}</h3>
                    <p style="color: #64748b; font-size: 0.9rem;">{value['desc']}</p>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Stats
    st.markdown("""
        <div style="background: linear-gradient(135deg, #818cf8 0%, #a78bfa 100%);
            border-radius: 20px; padding: 3rem; text-align: center; color: white;">
            <h2 style="margin-bottom: 2rem;">Our Journey So Far</h2>
    """, unsafe_allow_html=True)
    
    stat_cols = st.columns(4)
    stats = [
        ("100+", "Properties Listed"),
        ("50+", "Happy Customers"),
        ("50+", "Cities Covered"),
        ("100+", "Property Owners")
    ]
    
    for i, (num, label) in enumerate(stats):
        with stat_cols[i]:
            st.markdown(f"""
                <div style="text-align: center;margin-top : 10px;">
                    <div style="font-size: 2.5rem; font-weight: 700;">{num}</div>
                    <div style="opacity: 0.9;">{label}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Team Section
    st.markdown("""
        <h2 style="text-align: center; margin: 3rem 0 2rem;">Meet Our Team</h2>
    """, unsafe_allow_html=True)
    
    team = [
        {"name": "Tirth Antala", "role": "Founder & CEO", "initial": "T"},
        {"name": "Naimish Gondaliya", "role": "Head of Operations", "initial": "N"},
        {"name": "Chirag solanki", "role": "Tech Lead", "initial": "C"},
    ]
    
    team_cols = st.columns(3)
    for i, member in enumerate(team):
        with team_cols[i]:
            st.markdown(f"""
                <div style="text-align: center; padding: 1.5rem;margin-bottom : 20px;">
                    <div style="width: 80px; height: 80px; border-radius: 50%;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        display: flex; align-items: center; justify-content: center;
                        color: white; font-size: 2rem; font-weight: 600;
                        margin: 0 auto 1rem;">
                        {member['initial']}
                    </div>
                    <h4 style="margin: 0; font-weight: 600;">{member['name']}</h4>
                    <p style="color: #64748b; font-size: 0.9rem; margin: 0.25rem 0 0;">
                        {member['role']}
                    </p>
                </div>
            """, unsafe_allow_html=True)
    
    render_footer()
