"""
Property Recommendation System
"""
from database import db
from bson import ObjectId

def get_similar_properties(property_id: str, limit: int = 4) -> list:
    """Get similar properties based on type, city, and price range"""
    property_data = db.get_property_by_id(property_id)
    if not property_data:
        return []
    
    price = property_data.get("price", 0)
    price_range = (price * 0.7, price * 1.3)
    
    pipeline = [
        {
            "$match": {
                "_id": {"$ne": ObjectId(property_id)},
                "verified": True,
                "is_active": True,
                "$or": [
                    {"city": property_data.get("city")},
                    {"property_type": property_data.get("property_type")},
                    {"price": {"$gte": price_range[0], "$lte": price_range[1]}}
                ]
            }
        },
        {"$limit": limit}
    ]
    
    return list(db.db.properties.aggregate(pipeline))

def get_recommended_properties(user_id: str, limit: int = 6) -> list:
    """Get personalized recommendations based on user activity"""
    favorites = db.get_user_favorites(user_id)
    
    if not favorites:
        return list(db.db.properties.find(
            {"verified": True, "is_active": True}
        ).sort("views", -1).limit(limit))
    
    cities = list(set(p.get("city") for p in favorites))
    types = list(set(p.get("property_type") for p in favorites))
    favorite_ids = [p["_id"] for p in favorites]
    
    return list(db.db.properties.find({
        "_id": {"$nin": favorite_ids},
        "verified": True,
        "is_active": True,
        "$or": [
            {"city": {"$in": cities}},
            {"property_type": {"$in": types}}
        ]
    }).limit(limit))

def suggest_price(city: str, property_type: str, bedrooms: int, area: float, listing_type: str) -> dict:
    """Suggest price based on market data"""
    pipeline = [
        {
            "$match": {
                "city": city,
                "property_type": property_type,
                "listing_type": listing_type,
                "verified": True
            }
        },
        {
            "$group": {
                "_id": None,
                "avg_price": {"$avg": "$price"},
                "min_price": {"$min": "$price"},
                "max_price": {"$max": "$price"},
                "count": {"$sum": 1}
            }
        }
    ]
    
    result = list(db.db.properties.aggregate(pipeline))
    
    if not result:
        base_prices = {
            "buy": {"Flat": 5000000, "House": 8000000, "Villa": 15000000, "Plot": 3000000},
            "rent": {"Flat": 25000, "House": 40000, "Villa": 80000, "Studio": 15000}
        }
        base = base_prices.get(listing_type, base_prices["buy"]).get(property_type, 5000000)
        bedroom_factor = 1 + (bedrooms - 2) * 0.15 if bedrooms > 2 else 1
        
        return {
            "suggested_price": int(base * bedroom_factor),
            "min_range": int(base * bedroom_factor * 0.8),
            "max_range": int(base * bedroom_factor * 1.2),
            "based_on": 0
        }
    
    data = result[0]
    bedroom_factor = 1 + (bedrooms - 2) * 0.15 if bedrooms > 2 else 1
    
    return {
        "suggested_price": int(data["avg_price"] * bedroom_factor),
        "min_range": int(data["min_price"]),
        "max_range": int(data["max_price"]),
        "based_on": data["count"]
    }
