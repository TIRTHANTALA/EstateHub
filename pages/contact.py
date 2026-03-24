"""
Contact Page for EstateHub
"""
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pages.components import render_navbar, render_footer
from auth import is_logged_in, get_current_user

def send_contact_email(sender_name: str, sender_email: str, sender_phone: str, subject: str, message: str) -> bool:
    """
    Send contact form message to estatehub32@gmail.com
    
    - sender_email: User/Owner's email (used for Reply-To)
    - Receiver: estatehub32@gmail.com
    """
    try:
        # EstateHub email configuration
        estatehub_email = "estatehub32@gmail.com"
        smtp_password = "icat qpjp bbhr uprn"  # Gmail App Password
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = f"{sender_name} <{estatehub_email}>"  # Shows sender name
        msg['To'] = estatehub_email
        msg['Reply-To'] = sender_email  # Replies go to user/owner's email
        msg['Subject'] = f"[EstateHub] {subject} - from {sender_name}"
        
        # Email body with sender details
        body = f"""
NEW MESSAGE FROM ESTATEHUB CONTACT FORM
========================================

SENDER DETAILS:
---------------
Name    : {sender_name}
Email   : {sender_email}
Phone   : {sender_phone}

SUBJECT: {subject}

MESSAGE:
--------
{message}

----------------------------------------
To reply to {sender_name}, simply reply to this email.
Your reply will be sent to: {sender_email}
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email via Gmail SMTP
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(estatehub_email, smtp_password)
            server.sendmail(estatehub_email, estatehub_email, msg.as_string())
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def render_contact():
    """Render contact page"""
    render_navbar("Contact")
    
    st.markdown("""
        <div style="text-align: center; padding: 3rem 0;">
            <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e;">
                Contact Us
            </h1>
            <p style="color: #64748b; max-width: 600px; margin: 1rem auto;">
                Have questions? We'd love to hear from you. Send us a message and we'll 
                respond as soon as possible.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("""
            <div class="dashboard-card" style="padding: 2rem;margin-bottom: 2rem;">
                <h3 style="color: #1a1a2e; margin-bottom: 1.5rem;">Send us a Message</h3>
        """, unsafe_allow_html=True)
        
        # Auto-fill user details if logged in
        default_name = ""
        default_email = ""
        default_phone = ""
        
        if is_logged_in():
            user = get_current_user()
            if user:
                default_name = user.get("name", "")
                default_email = user.get("email", "")
                default_phone = user.get("phone", "")
        
        name = st.text_input("Your Name *", value=default_name, placeholder="Enter your full name")
        email = st.text_input("Email Address *", value=default_email, placeholder="Enter your email")
        phone = st.text_input("Phone Number", value=default_phone, placeholder="Enter your phone number")
        subject = st.selectbox("Subject", [
            "General Inquiry",
            "Property Listing Help",
            "Technical Support",
            "Report an Issue",
            "Partnership Inquiry",
            "Other"
        ])
        message = st.text_area("Message *", placeholder="Type your message here...", height=150)
        
        if st.button("📧 Send Message", type="primary", use_container_width=True):
            if not name or not email or not message:
                st.error("Please fill in all required fields (Name, Email, Message)")
            else:
                if send_contact_email(name, email, phone, subject, message):
                    st.success(f"✅ Message sent successfully! We'll reply to {email} within 24 hours.")
                else:
                    st.error("❌ Failed to send message. Please try again or email us directly at estatehub32@gmail.com")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        # Contact Info Cards
        st.markdown("""
            <div class="dashboard-card" style="padding: 1.5rem; margin-bottom: 2rem;">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="width: 50px; height: 50px; border-radius: 12px;
                        background: #f0f1ff; display: flex; align-items: center;
                        justify-content: center; font-size: 1.5rem;">📍</div>
                    <div>
                        <h4 style="margin: 0; font-weight: 600;">Address</h4>
                        <p style="color: #64748b; margin: 0.25rem 0 0; font-size: 0.9rem;">
                            Ahmedabad, Gujarat, India
                        </p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="dashboard-card" style="padding: 1.5rem; margin-bottom: 2rem;">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="width: 50px; height: 50px; border-radius: 12px;
                        background: #f0f1ff; display: flex; align-items: center;
                        justify-content: center; font-size: 1.5rem;">📞</div>
                    <div>
                        <h4 style="margin: 0; font-weight: 600;">Phone</h4>
                        <p style="color: #64748b; margin: 0.25rem 0 0; font-size: 0.9rem;">
                            +91 7984087441<br>
                            Mon-Sat, 9AM-6PM
                        </p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="dashboard-card" style="padding: 1.5rem; margin-bottom: 2rem;">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="width: 50px; height: 50px; border-radius: 12px;
                        background: #f0f1ff; display: flex; align-items: center;
                        justify-content: center; font-size: 1.5rem;">✉️</div>
                    <div>
                        <h4 style="margin: 0; font-weight: 600;">Email</h4>
                        <p style="color: #64748b; margin: 0.25rem 0 0; font-size: 0.9rem;">
                            estatehub32@gmail.com
                        </p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # FAQ Section
    st.markdown("""
        <h2 style="text-align: center; margin: 3rem 0 2rem;">Frequently Asked Questions</h2>
    """, unsafe_allow_html=True)
    
    faqs = [
        {
            "q": "How do I list my property on EstateHub?",
            "a": "Simply register as a property owner, verify your account, and click on 'Add Property' in your dashboard. Fill in the property details, upload images, and submit for verification."
        },
        {
            "q": "How long does property verification take?",
            "a": "Our team typically verifies properties within 24-48 hours. You'll receive a notification once your property is verified and live on the platform."
        },
        {
            "q": "Is there any fee for listing properties?",
            "a": "Basic listings are free! We also offer premium listing options for better visibility. Contact us for enterprise pricing."
        },
        {
            "q": "How do I schedule a property visit?",
            "a": "Once you find a property you like, click on 'Book Visit' and select your preferred date and time. The owner will confirm the appointment."
        },
        {
            "q": "Can I edit my listing after publishing?",
            "a": "Yes, you can edit your listings anytime from your owner dashboard. Major changes may require re-verification."
        }
    ]
    
    for faq in faqs:
        with st.expander(faq["q"]):
            st.write(faq["a"])
    
    render_footer()
