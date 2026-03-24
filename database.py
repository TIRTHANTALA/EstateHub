
"""
Database connection and operations for EstateHub
"""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime
from bson import ObjectId
import config

class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        try:
            self.client = MongoClient(config.MONGO_URI)
            self.client.admin.command('ping')
            self.db = self.client[config.DATABASE_NAME]
            self._initialized = True
            self._setup_collections()
        except ConnectionFailure:
            print("Failed to connect to MongoDB")
            self.db = None
    
    def _setup_collections(self):
        """Initialize collections and indexes"""
        if self.db is None:
            return
        
        # Create indexes
        if "users" in self.db.list_collection_names():
            self.db.users.create_index("email", unique=True)
        if "properties" in self.db.list_collection_names():
            self.db.properties.create_index([("city", 1), ("property_type", 1)])
            self.db.properties.create_index("owner_id")
    
    # User Operations
    def create_user(self, user_data: dict) -> str:
        user_data["created_at"] = datetime.utcnow()
        user_data["is_active"] = True
        result = self.db.users.insert_one(user_data)
        return str(result.inserted_id)
    
    def get_user_by_email(self, email: str) -> dict:
        return self.db.users.find_one({"email": email.lower()})
    
    def get_user_by_id(self, user_id: str) -> dict:
        return self.db.users.find_one({"_id": ObjectId(user_id)})
    
    def update_user(self, user_id: str, update_data: dict) -> bool:
        result = self.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    def get_all_users(self, role: str = None) -> list:
        query = {}
        if role:
            query["role"] = role
        return list(self.db.users.find(query))
    
    def count_users(self, role: str = None) -> int:
        query = {}
        if role:
            query["role"] = role
        return self.db.users.count_documents(query)
    
    def block_user(self, user_id: str) -> bool:
        return self.update_user(user_id, {"is_active": False})
    
    def unblock_user(self, user_id: str) -> bool:
        return self.update_user(user_id, {"is_active": True})
    
    # Property Operations
    def create_property(self, property_data: dict) -> str:
        property_data["created_at"] = datetime.utcnow()
        property_data["verified"] = False
        property_data["is_active"] = True
        property_data["views"] = 0
        result = self.db.properties.insert_one(property_data)
        return str(result.inserted_id)
    
    def get_property_by_id(self, property_id: str) -> dict:
        return self.db.properties.find_one({"_id": ObjectId(property_id)})
    
    def get_properties(self, filters: dict = None, sort_by: str = "newest", limit: int = 50) -> list:
        query = {"is_active": True, "verified": True}
        if filters:
            if filters.get("city") and filters["city"] != "All Cities":
                query["city"] = filters["city"]
            if filters.get("property_type") and filters["property_type"] != "All Types":
                query["property_type"] = filters["property_type"]
            if filters.get("listing_type") and filters["listing_type"] != "All":
                query["listing_type"] = filters["listing_type"]
            if filters.get("bedrooms"):
                query["bedrooms"] = filters["bedrooms"]
            if filters.get("min_price"):
                query["price"] = {"$gte": filters["min_price"]}
            if filters.get("max_price"):
                if "price" in query:
                    query["price"]["$lte"] = filters["max_price"]
                else:
                    query["price"] = {"$lte": filters["max_price"]}
        
        sort_order = [("created_at", -1)]
        if sort_by == "price_low":
            sort_order = [("price", 1)]
        elif sort_by == "price_high":
            sort_order = [("price", -1)]
        
        return list(self.db.properties.find(query).sort(sort_order).limit(limit))
    
    def get_properties_by_owner(self, owner_id: str) -> list:
        return list(self.db.properties.find({"owner_id": owner_id}))
    
    def get_all_properties(self, verified_only: bool = False) -> list:
        query = {}
        if verified_only:
            query["verified"] = True
        return list(self.db.properties.find(query))
    
    def update_property(self, property_id: str, update_data: dict) -> bool:
        result = self.db.properties.update_one(
            {"_id": ObjectId(property_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    def delete_property(self, property_id: str) -> bool:
        result = self.db.properties.delete_one({"_id": ObjectId(property_id)})
        return result.deleted_count > 0
    
    def verify_property(self, property_id: str) -> bool:
        return self.update_property(property_id, {"verified": True})
    
    def increment_views(self, property_id: str):
        self.db.properties.update_one(
            {"_id": ObjectId(property_id)},
            {"$inc": {"views": 1}}
        )
    
    def count_properties(self, verified_only: bool = False) -> int:
        query = {}
        if verified_only:
            query["verified"] = True
        return self.db.properties.count_documents(query)
    
    def get_popular_cities(self) -> list:
        pipeline = [
            {"$match": {"verified": True, "is_active": True}},
            {"$group": {"_id": "$city", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 6}
        ]
        return list(self.db.properties.aggregate(pipeline))
    
    # Favorites Operations
    def add_favorite(self, user_id: str, property_id: str, user_role: str = "user") -> bool:
        existing = self.db.favorites.find_one({
            "user_id": user_id,
            "property_id": property_id
        })
        if existing:
            return False
        self.db.favorites.insert_one({
            "user_id": user_id,
            "property_id": property_id,
            "user_role": user_role,  # Track which role favorited
            "created_at": datetime.utcnow()
        })
        return True
    
    def remove_favorite(self, user_id: str, property_id: str) -> bool:
        result = self.db.favorites.delete_one({
            "user_id": user_id,
            "property_id": property_id
        })
        return result.deleted_count > 0
    
    def get_user_favorites(self, user_id: str) -> list:
        favorites = self.db.favorites.find({"user_id": user_id})
        property_ids = [ObjectId(f["property_id"]) for f in favorites]
        return list(self.db.properties.find({"_id": {"$in": property_ids}}))
    
    def get_user_favorites_with_role(self, user_id: str) -> list:
        """Get favorites with role information"""
        favorites = list(self.db.favorites.find({"user_id": user_id}))
        property_ids = [ObjectId(f["property_id"]) for f in favorites]
        properties = list(self.db.properties.find({"_id": {"$in": property_ids}}))
        
        # Add role information to each property
        for prop in properties:
            prop_id = str(prop["_id"])
            for fav in favorites:
                if fav["property_id"] == prop_id:
                    prop["favorited_by_role"] = fav.get("user_role", "user")
                    break
        return properties
    
    def is_favorite(self, user_id: str, property_id: str) -> bool:
        return self.db.favorites.find_one({
            "user_id": user_id,
            "property_id": property_id
        }) is not None
    
    # Visit Request Operations
    def create_visit(self, visit_data: dict) -> str:
        visit_data["created_at"] = datetime.utcnow()
        visit_data["status"] = "pending"
        result = self.db.visits.insert_one(visit_data)
        return str(result.inserted_id)
    
    def get_visits_for_owner(self, owner_id: str) -> list:
        return list(self.db.visits.find({"owner_id": owner_id}).sort("created_at", -1))
    
    def get_visits_by_user(self, user_id: str) -> list:
        return list(self.db.visits.find({"user_id": user_id}).sort("created_at", -1))
    
    def get_visits_by_user_with_details(self, user_id: str) -> list:
        """Get visit requests with property details"""
        visits = list(self.db.visits.find({"user_id": user_id}).sort("created_at", -1))
        
        # Add property details to each visit
        for visit in visits:
            property_id = visit.get("property_id")
            if property_id:
                property_data = self.get_property_by_id(property_id)
                visit["property_details"] = property_data
        
        return visits
    
    def update_visit_status(self, visit_id: str, status: str) -> bool:
        result = self.db.visits.update_one(
            {"_id": ObjectId(visit_id)},
            {"$set": {"status": status, "updated_at": datetime.utcnow()}}
        )
        return result.modified_count > 0
    
    def count_pending_visits(self, owner_id: str) -> int:
        return self.db.visits.count_documents({
            "owner_id": owner_id,
            "status": "pending"
        })
    
    # OTP Operations
    def save_otp(self, email: str, otp: str, expiry: 'datetime') -> bool:
        """Save OTP for password reset"""
        self.db.otp_tokens.delete_many({"email": email.lower()})  # Remove old OTPs
        self.db.otp_tokens.insert_one({
            "email": email.lower(),
            "otp": otp,
            "expiry": expiry,
            "created_at": datetime.utcnow()
        })
        return True
    
    def verify_otp(self, email: str, otp: str) -> tuple:
        """Verify OTP and return (success, message)"""
        record = self.db.otp_tokens.find_one({"email": email.lower(), "otp": otp})
        if not record:
            return False, "Invalid OTP"
        if datetime.utcnow() > record["expiry"]:
            self.db.otp_tokens.delete_one({"_id": record["_id"]})
            return False, "OTP has expired"
        return True, "OTP verified"
    
    def delete_otp(self, email: str) -> bool:
        """Delete OTP after successful password reset"""
        self.db.otp_tokens.delete_many({"email": email.lower()})
        return True
    
    def update_password(self, email: str, new_password_hash: str) -> bool:
        """Update user password"""
        result = self.db.users.update_one(
            {"email": email.lower()},
            {"$set": {"password": new_password_hash}}
        )
        return result.modified_count > 0
    
    # Admin Operations
    def get_admin_by_email(self, email: str) -> dict:
        return self.db.admins.find_one({"email": email.lower()})
    
    def create_admin(self, admin_data: dict) -> str:
        admin_data["created_at"] = datetime.utcnow()
        result = self.db.admins.insert_one(admin_data)
        return str(result.inserted_id)
    
    # Analytics
    def get_analytics(self) -> dict:
        return {
            "total_users": self.count_users(),
            "total_owners": self.count_users("owner"),
            "total_buyers": self.count_users("user"),
            "total_properties": self.count_properties(),
            "verified_properties": self.count_properties(verified_only=True),
            "pending_properties": self.db.properties.count_documents({"verified": False}),
            "total_visits": self.db.visits.count_documents({}),
            "popular_cities": self.get_popular_cities()
        }


# Global database instance
db = Database()
