"""
Helper utilities for EstateHub
"""
import streamlit as st
from datetime import datetime
import base64
from io import BytesIO

def format_price(price: float, listing_type: str = "buy") -> str:
    """Format price in Indian currency format"""
    if listing_type == "rent":
        if price >= 100000:
            return f"₹{price/100000:.1f} Lakh/mo"
        elif price >= 1000:
            return f"₹{price/1000:.0f}K/mo"
        else:
            return f"₹{price:.0f}/mo"
    else:
        if price >= 10000000:
            return f"₹{price/10000000:.2f} Cr"
        elif price >= 100000:
            return f"₹{price/100000:.2f} Lakh"
        else:
            return f"₹{price:,.0f}"

def format_date(date) -> str:
    """Format datetime to readable string"""
    if isinstance(date, datetime):
        return date.strftime("%d %b %Y")
    return str(date)

def time_ago(date) -> str:
    """Get relative time string"""
    if not isinstance(date, datetime):
        return ""
    
    now = datetime.utcnow()
    diff = now - date
    
    if diff.days > 30:
        return f"{diff.days // 30} months ago"
    elif diff.days > 0:
        return f"{diff.days} days ago"
    elif diff.seconds > 3600:
        return f"{diff.seconds // 3600} hours ago"
    elif diff.seconds > 60:
        return f"{diff.seconds // 60} minutes ago"
    else:
        return "Just now"

def get_property_image_placeholder(property_type: str) -> str:
    """Get placeholder image URL based on property type"""
    placeholders = {
        "Flat": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=400",
        "House": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400",
        "Villa": "https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=400",
        "Plot": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=400",
        "Penthouse": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=400",
        "Studio": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=400"
    }
    return placeholders.get(property_type, placeholders["Flat"])

def show_success(message: str):
    """Show success message"""
    st.success(message)

def show_error(message: str):
    """Show error message"""
    st.error(message)

def show_info(message: str):
    """Show info message"""
    st.info(message)

def show_warning(message: str):
    """Show warning message"""
    st.warning(message)

def validate_email(email: str) -> bool:
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """Basic phone validation"""
    import re
    pattern = r'^[6-9]\d{9}$'
    clean_phone = phone.replace(" ", "").replace("-", "")
    return re.match(pattern, clean_phone) is not None

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def image_to_base64(uploaded_file, max_size=(800, 600), quality=70) -> str:
    """Convert uploaded image file to compressed base64 string"""
    if uploaded_file is None:
        return None
    
    try:
        from PIL import Image
        from io import BytesIO
        
        # Open image
        img = Image.open(uploaded_file)
        
        # Convert to RGB if necessary (for PNG with transparency and AVIF)
        if img.mode in ('RGBA', 'P', 'LA'):
            img = img.convert('RGB')
        
        # Resize if larger than max_size
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Compress and save to bytes
        buffer = BytesIO()
        
        # Determine output format based on input
        file_type = getattr(uploaded_file, 'type', '').lower() or ''
        if 'avif' in file_type or uploaded_file.name.lower().endswith('.avif'):
            # For AVIF files, save as JPEG for better compatibility
            img.save(buffer, format='JPEG', quality=quality, optimize=True)
            file_format = 'jpeg'
        else:
            # For other formats, save as JPEG
            img.save(buffer, format='JPEG', quality=quality, optimize=True)
            file_format = 'jpeg'
        
        buffer.seek(0)
        
        # Convert to base64
        base64_str = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/{file_format};base64,{base64_str}"
    
    except Exception as e:
        # Fallback to original method if PIL fails
        uploaded_file.seek(0)
        bytes_data = uploaded_file.getvalue()
        base64_str = base64.b64encode(bytes_data).decode()
        file_type = uploaded_file.type.split('/')[-1] if hasattr(uploaded_file, 'type') else 'jpeg'
        return f"data:image/{file_type};base64,{base64_str}"

def process_multiple_images(uploaded_files) -> list:
    """Process multiple uploaded images and return list of base64 strings"""
    images = []
    if uploaded_files:
        for file in uploaded_files:
            if file is not None:
                img_base64 = image_to_base64(file)
                if img_base64:
                    images.append(img_base64)
    return images

def get_image_html(image_data: str, placeholder: str, style: str = "") -> str:
    """Get image HTML with fallback to placeholder"""
    if image_data and image_data.startswith("data:image"):
        return f'<img src="{image_data}" style="{style}" alt="Property">'
    elif image_data and image_data.startswith("http"):
        return f'<img src="{image_data}" style="{style}" onerror="this.src=\'{placeholder}\'" alt="Property">'
    else:
        return f'<img src="{placeholder}" style="{style}" alt="Property">'
