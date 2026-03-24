# 🏠 EstateHub - Real Estate Platform

A complete Real Estate Buy & Rent Platform built with Python, Streamlit, and MongoDB.

![EstateHub](https://img.shields.io/badge/Python-3.9+-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red) ![MongoDB](https://img.shields.io/badge/MongoDB-4.4+-green)

## 🎯 Features

### For Buyers/Tenants
- 🔍 Search and filter properties
- ❤️ Save favorite properties
- 📅 Book property visits
- 👤 User profile management

### For Property Owners
- 📝 List new properties
- 💡 AI-powered price suggestions
- 📊 Manage listings
- ✅ Handle visit requests

### For Admins
- 🛡️ Verify property listings
- 👥 User management
- 📈 Platform analytics
- 🚫 Block fake users

## 🛠️ Tech Stack

- **Frontend**: Streamlit (Python)
- **Backend**: Python
- **Database**: MongoDB
- **Styling**: Custom CSS

## 📋 Prerequisites

- Python 3.9+
- MongoDB (local or Atlas)
- pip package manager

## 🚀 Installation

1. **Clone the repository**
```bash
cd estateease
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
# Copy example env file
copy .env.example .env

# Edit .env with your MongoDB URI
```

5. **Start MongoDB**
```bash
# If using local MongoDB
mongod
```

6. **Setup database with sample data**
```bash
python setup_database.py
```

7. **Run the application**
```bash
streamlit run app.py
```

8. **Open in browser**
```
http://localhost:8501
```

## 🔐 Login Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@estateease.com | admin123 |
| User | rahul@example.com | user123 |
| Owner | amit@example.com | owner123 |

## 📁 Project Structure

```
estateease/
│
├── app.py                 # Main application entry
├── config.py              # Configuration settings
├── database.py            # MongoDB operations
├── auth.py                # Authentication logic
├── setup_database.py      # Database initialization
├── requirements.txt       # Python dependencies
│
├── pages/                 # UI Pages
│   ├── components.py      # Reusable UI components
│   ├── home.py           # Home page
│   ├── login.py          # Login page
│   ├── register.py       # Registration page
│   ├── properties.py     # Property listings
│   ├── property_detail.py# Property details
│   ├── dashboard.py      # User dashboard
│   ├── owner_dashboard.py# Owner dashboard
│   └── admin_dashboard.py# Admin dashboard
│
└── utils/                 # Utilities
    ├── styles.py         # Custom CSS
    ├── helpers.py        # Helper functions
    ├── filters.py        # Filter utilities
    └── recommendations.py # Recommendation engine
```

## 🗄️ Database Schema

### Users Collection
```json
{
  "_id": "ObjectId",
  "name": "string",
  "email": "string",
  "phone": "string",
  "password": "hashed_string",
  "role": "user|owner",
  "is_active": "boolean",
  "created_at": "datetime"
}
```

### Properties Collection
```json
{
  "_id": "ObjectId",
  "title": "string",
  "description": "string",
  "property_type": "Flat|House|Villa|Plot|Penthouse|Studio",
  "city": "string",
  "listing_type": "buy|rent",
  "price": "number",
  "bedrooms": "number",
  "bathrooms": "number",
  "area": "number",
  "furnishing": "string",
  "amenities": ["array"],
  "image": "string",
  "owner_id": "string",
  "verified": "boolean",
  "is_active": "boolean",
  "views": "number",
  "created_at": "datetime"
}
```

### Visits Collection
```json
{
  "_id": "ObjectId",
  "user_id": "string",
  "owner_id": "string",
  "property_id": "string",
  "property_title": "string",
  "visit_date": "string",
  "visit_time": "string",
  "message": "string",
  "status": "pending|approved|rejected",
  "created_at": "datetime"
}
```

## 🎨 UI Features

- Modern purple gradient theme
- Responsive design
- Property cards with hover effects
- Interactive filters
- Dashboard statistics
- Clean forms with validation

## 🔮 Smart Features

1. **Price Suggestion Engine**: AI-powered price recommendations based on market data
2. **Similar Properties**: Recommends similar properties based on type, city, and price
3. **Personalized Recommendations**: Based on user's saved properties
4. **Popular Cities Analytics**: Shows trending cities with most listings

## 📝 College Project Documentation

### Abstract
EstateHub is a comprehensive real estate platform that connects property buyers, tenants, and owners. Built using modern Python technologies, it provides a seamless experience for property discovery, listing, and management.

### Problem Statement
The traditional property search process is fragmented, time-consuming, and often lacks transparency. Users struggle to find verified properties, compare options, and connect with genuine owners. Property owners face difficulties in reaching potential buyers/tenants efficiently.

### Solution
EstateHub solves these problems by providing:
- Centralized platform for property discovery
- Verified listings to ensure authenticity
- Direct owner-buyer communication
- Easy property management for owners
- Admin oversight for quality control

### Future Scope
1. Mobile application (Flutter/React Native)
2. Virtual property tours (360° images)
3. AI-powered property valuation
4. Document verification system
5. Payment gateway integration
6. Chat system between users and owners
7. Property comparison feature
8. Neighborhood analytics
9. EMI calculator
10. Legal documentation assistance

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Built with ❤️ for educational purposes

---

**⭐ Star this repository if you found it helpful!**
