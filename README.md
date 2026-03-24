# 🏠 EstateHub - Real Estate Platform

A complete Real Estate Buy & Rent Platform built with Python, Streamlit, and MongoDB.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![MongoDB](https://img.shields.io/badge/MongoDB-4.4+-green)
<img width="1410" height="940" alt="image" src="https://github.com/user-attachments/assets/93d6b873-8c0d-45f3-a7e1-3984661fefea" />

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
- **Frontend:** Streamlit (Python)
- **Backend:** Python
- **Database:** MongoDB
- **Styling:** Custom CSS

## 📋 Prerequisites
- Python 3.9+
- MongoDB (local or Atlas)
- pip package manager

## 🚀 How to Run

1. Clone the repo
   git clone https://github.com/TIRTHANTALA/EstateHub.git

2. Install dependencies
   pip install -r requirements.txt

3. Add your MongoDB URI in .env file
   MONGO_URI=mongodb://localhost:27017/

4. Run the app
   streamlit run app.py

## 🔐 Login Credentials

| Role  | Email                    | Password |
|-------|--------------------------|----------|
| Admin | admin@estateease.com     | admin123 |
| User  | rahul@example.com        | user123  |
| Owner | amit@example.com         | owner123 |

## 📁 Project Structure
```
EstateHub/
├── app.py              # Main application entry
├── config.py           # Configuration settings
├── database.py         # MongoDB operations
├── auth.py             # Authentication logic
├── requirements.txt    # Python dependencies
├── pages/              # UI Pages
│   ├── home.py
│   ├── login.py
│   ├── register.py
│   ├── properties.py
│   ├── dashboard.py
│   ├── owner_dashboard.py
│   └── admin_dashboard.py
└── utils/              # Utilities
    ├── styles.py
    ├── helpers.py
    └── filters.py
```

## 👨‍💻 Author
Built with ❤️ for educational purposes
