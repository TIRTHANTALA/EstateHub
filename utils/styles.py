"""
Custom CSS Styles for EstateHub
Light theme with purple accents
"""

def get_custom_css():
    return """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Force Light Theme */
    .stApp {
        font-family: 'Inter', sans-serif;
        background-color: #ffffff !important;
        color: #1a1a2e !important;
    }
    
    /* Override Streamlit dark mode */
    .stApp > header {
        background-color: #ffffff !important;
    }
    
    [data-testid="stAppViewContainer"] {
        background-color: #f8fafc !important;
    }
    
    [data-testid="stHeader"] {
        background-color: #ffffff !important;
    }
    
    .main .block-container {
        background-color: #f8fafc !important;
    }
    
    /* All text should be dark */
    p, span, div, h1, h2, h3, h4, h5, h6, label {
        color: #1a1a2e !important;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Logo */
    .logo-text {
        font-size: 1.8rem;
        font-weight: 700;
        color: #6366f1 !important;
    }
    
    /* Hero Section */
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        color: #1a1a2e !important;
        line-height: 1.2;
        margin-bottom: 1rem;
    }
    
    .hero-title span {
        color: #6366f1 !important;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: #64748b !important;
        margin-bottom: 2rem;
    }
    
    /* Purple Gradient Box */
    .purple-gradient-box {
        background: linear-gradient(135deg, #818cf8 0%, #a78bfa 100%);
        border-radius: 20px;
        padding: 2rem;
        color: white !important;
        text-align: center;
    }
    
    /* Property Cards */
    .property-card {
        background: #ffffff !important;
        border-radius: 16px;
        padding: 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        overflow: hidden;
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }
    
    .property-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.15);
    }
    
    .property-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
    }
    
    .property-content {
        padding: 1.5rem;
        background: #ffffff !important;
    }
    
    .property-price {
        font-size: 1.5rem;
        font-weight: 700;
        color: #6366f1 !important;
    }
    
    .property-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1a1a2e !important;
        margin: 0.5rem 0;
    }
    
    .property-location {
        color: #64748b !important;
        font-size: 0.9rem;
    }
    
    .property-features {
        display: flex;
        gap: 1rem;
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid #e2e8f0;
    }
    
    .feature-item {
        display: flex;
        align-items: center;
        gap: 0.3rem;
        color: #64748b !important;
        font-size: 0.85rem;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 10px !important;
        padding: 0.6rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
        background-color: #ffffff !important;
        color: #1a1a2e !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    .stButton > button:hover {
        border-color: #6366f1 !important;
        color: #6366f1 !important;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
    }
    
    /* Form Inputs */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stTextArea > div > div > textarea {
        border-radius: 10px !important;
        border: 1px solid #e2e8f0 !important;
        background-color: #ffffff !important;
        color: #1a1a2e !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #94a3b8 !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
    }
    
    /* Selectbox dropdown */
    [data-baseweb="select"] {
        background-color: #ffffff !important;
    }
    
    [data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border-color: #e2e8f0 !important;
    }
    
    [data-baseweb="popover"] {
        background-color: #ffffff !important;
    }
    
    [data-baseweb="menu"] {
        background-color: #ffffff !important;
    }
    
    [role="option"] {
        background-color: #ffffff !important;
        color: #1a1a2e !important;
    }
    
    [role="option"]:hover {
        background-color: #f1f5f9 !important;
    }
    
    /* Cards */
    .info-card {
        background: #ffffff !important;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    
    .info-card-icon {
        width: 60px;
        height: 60px;
        border-radius: 12px;
        background: #f0f1ff !important;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1rem;
        font-size: 1.5rem;
        color: #6366f1 !important;
    }
    
    .info-card-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1a1a2e !important;
        margin-bottom: 0.5rem;
    }
    
    .info-card-text {
        color: #64748b !important;
        font-size: 0.9rem;
    }
    
    /* Stats */
    .stat-box {
        text-align: center;
        padding: 1rem;
        background: #ffffff !important;
        border-radius: 12px;
        border: none !important;
        box-shadow: none !important;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a2e !important;
    }
    
    .stat-label {
        color: #64748b !important;
        font-size: 0.9rem;
    }
    
    /* Remove column borders/lines */
    [data-testid="column"] {
        border: none !important;
        box-shadow: none !important;
    }
    
    /* Remove stVerticalBlock border */
    [data-testid="stVerticalBlock"] {
        border: none !important;
        gap: 0 !important;
    }
    
    /* Remove any divider lines from horizontal blocks */
    [data-testid="stHorizontalBlock"] {
        border: none !important;
        border-bottom: none !important;
    }
    
    /* Login/Register Cards */
    .auth-card {
        background: #ffffff !important;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        max-width: 450px;
        margin: 0 auto;
    }
    
    .auth-header {
        background: linear-gradient(135deg, #818cf8 0%, #a78bfa 100%);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        color: white !important;
        margin-bottom: 1.5rem;
    }
    
    .auth-title {
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: white !important;
    }
    
    .auth-subtitle {
        opacity: 0.9;
        font-size: 0.95rem;
        color: white !important;
    }
    
    /* Dashboard */
    .dashboard-card {
        background: #ffffff !important;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        border: 1px solid #e2e8f0;
    }
    
    .dashboard-stat {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 1.5rem;
        color: white !important;
    }
    
    .dashboard-stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: white !important;
    }
    
    .dashboard-stat-label {
        opacity: 0.9;
        font-size: 0.9rem;
        color: white !important;
    }
    
    /* Sidebar */
    .sidebar-section {
        background: #ffffff !important;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid #e2e8f0;
    }
    
    .sidebar-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1a1a2e !important;
        margin-bottom: 1rem;
    }
    
    /* Footer */
    .footer {
        background: #1a1a2e !important;
        color: white !important;
        padding: 3rem 2rem;
        margin-top: 3rem;
    }
    
    .footer-logo {
        font-size: 1.5rem;
        font-weight: 700;
        color: #6366f1 !important;
        margin-bottom: 1rem;
    }
    
    .footer-links {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    
    .footer-link {
        color: #94a3b8 !important;
        text-decoration: none;
        font-size: 0.9rem;
    }
    
    /* Verified Badge */
    .verified-badge {
        background: #10b981 !important;
        color: white !important;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 500;
    }
    
    .pending-badge {
        background: #f59e0b !important;
        color: white !important;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 500;
    }
    
    /* Rating */
    .rating-box {
        background: #ffffff !important;
        border-radius: 12px;
        padding: 0.5rem 1rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .rating-star {
        color: #fbbf24 !important;
    }
    
    /* CTA Section */
    .cta-section {
        background: linear-gradient(135deg, #818cf8 0%, #a78bfa 100%);
        border-radius: 20px;
        padding: 3rem;
        text-align: center;
        color: white !important;
        margin: 2rem 0;
    }
    
    .cta-section h2, .cta-section p {
        color: white !important;
    }
    
    .cta-title {
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: white !important;
    }
    
    .cta-subtitle {
        opacity: 0.9;
        margin-bottom: 1.5rem;
        color: white !important;
    }
    
    /* Testimonials */
    .testimonial-card {
        background: #ffffff !important;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        border: 1px solid #e2e8f0;
    }
    
    .testimonial-stars {
        color: #fbbf24 !important;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    
    .testimonial-text {
        color: #64748b !important;
        font-style: italic;
        margin-bottom: 1rem;
    }
    
    .testimonial-author {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .testimonial-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white !important;
        font-weight: 600;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: transparent !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.5rem 1rem;
        font-weight: 500;
        background-color: transparent !important;
        color: #64748b !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        border-radius: 8px;
        color: white !important;
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        background-color: #ffffff !important;
    }
    
    /* Metrics */
    [data-testid="stMetric"] {
        background: #ffffff !important;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
    }
    
    [data-testid="stMetricLabel"] {
        color: #64748b !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #1a1a2e !important;
    }
    
    /* Filter Section */
    .filter-section {
        background: #ffffff !important;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    }
    
    /* Search Box */
    .search-box {
        background: #ffffff !important;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        margin-top: -3rem;
        position: relative;
        z-index: 10;
    }
    
    /* Remove ALL horizontal lines/dividers */
    hr {
        display: none !important;
        border: none !important;
        height: 0 !important;
        margin: 0 !important;
    }
    
    /* Hide all streamlit dividers */
    [data-testid="stHorizontalBlock"] + hr,
    .element-container + hr,
    .stMarkdown hr,
    div[data-testid="stMarkdownContainer"] hr {
        display: none !important;
        border: none !important;
        height: 0 !important;
    }
    
    /* Remove any borders that look like lines */
    .stat-box {
        border: none !important;
    }
    
    /* Hide markdown generated hr elements */
    .stApp hr,
    .main hr,
    .block-container hr {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #ffffff !important;
        color: #1a1a2e !important;
    }
    
    .streamlit-expanderContent {
        background-color: #ffffff !important;
    }
    
    /* Alert boxes */
    .stAlert {
        background-color: #ffffff !important;
        border-radius: 10px;
    }
    
    /* Dataframe */
    .stDataFrame {
        background-color: #ffffff !important;
    }
    
    /* Columns background */
    [data-testid="column"] {
        background-color: transparent !important;
    }
    
    /* Markdown container */
    .stMarkdown {
        color: #1a1a2e !important;
    }
    
    /* Labels */
    .stSelectbox label, .stTextInput label, .stTextArea label {
        color: #1a1a2e !important;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }
        
        .cta-title {
            font-size: 1.5rem;
        }
    }
    </style>
    """

def inject_css():
    """Inject custom CSS into Streamlit app"""
    import streamlit as st
    st.markdown(get_custom_css(), unsafe_allow_html=True)
