"""
EstateHub Configuration
"""
import os

# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DATABASE_NAME = "RealEstate1"

# App Configuration
APP_NAME = "EstateHub"
APP_TAGLINE = "Find Your Dream Home With Ease"
VERSION = "1.0.0"

# Cities List
CITIES = [
    "Ahmedabad", "Surat", "Rajkot", "Mumbai", "Delhi",
    "Gandhinagar", "Vadodara", "Bangalore", "Pune", "Goa", "Kolkata"
]

# Property Types
PROPERTY_TYPES = ["Flat", "House", "Villa", "Plot", "Penthouse", "Studio", "Farm House"]

# Availability Status
AVAILABILITY_STATUS = ["Ready to Move", "Under Construction"]

# Ownership Types
OWNERSHIP_TYPES = ["Freehold", "Leasehold", "Co-operative Society", "Power of Attorney"]

# Facing Directions
FACING_DIRECTIONS = ["East", "West", "North", "South", "North-East", "North-West", "South-East", "South-West"]

# Age of Property
PROPERTY_AGE = ["Under Construction", "Less than 1 year", "1-3 years", "3-5 years", "5-10 years", "More than 10 years"]

# Floor Options
FLOOR_OPTIONS = ["Ground", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "10+", "Top Floor"]

# Budget Ranges
BUDGET_RANGES = {
    "Any Budget": (0, float('inf')),
    "Under ₹25 Lakh": (0, 2500000),
    "₹25-50 Lakh": (2500000, 5000000),
    "₹50 Lakh - 1 Cr": (5000000, 10000000),
    "₹1-2 Cr": (10000000, 20000000),
    "Above ₹2 Cr": (20000000, float('inf'))
}

# Rent Budget Ranges
RENT_BUDGET_RANGES = {
    "Any Budget": (0, float('inf')),
    "Under ₹10K": (0, 10000),
    "₹10K-25K": (10000, 25000),
    "₹25K-50K": (25000, 50000),
    "₹50K-1 Lakh": (50000, 100000),
    "Above ₹1 Lakh": (100000, float('inf'))
}

# Session Keys
SESSION_USER = "user"
SESSION_ROLE = "role"
SESSION_LOGGED_IN = "logged_in"

# Email Configuration (Gmail SMTP)
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "estatehub32@gmail.com")  # Your Gmail address
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "icat qpjp bbhr uprn")  # Your Gmail App Password

# OTP Settings
OTP_EXPIRY_MINUTES = 10
