"""
Filter utilities for property search
"""
import config

def build_filter_query(
    city: str = None,
    property_type: str = None,
    listing_type: str = None,
    bedrooms: int = None,
    budget_range: str = None,
    listing_type_for_budget: str = "buy"
) -> dict:
    """Build MongoDB filter query from user selections"""
    filters = {}
    
    if city and city != "All Cities":
        filters["city"] = city
    
    if property_type and property_type != "All Types":
        filters["property_type"] = property_type
    
    if listing_type and listing_type != "All":
        filters["listing_type"] = listing_type.lower()
    
    if bedrooms and bedrooms > 0:
        filters["bedrooms"] = bedrooms
    
    if budget_range and budget_range != "Any Budget":
        if listing_type_for_budget == "rent":
            budget_ranges = config.RENT_BUDGET_RANGES
        else:
            budget_ranges = config.BUDGET_RANGES
        
        if budget_range in budget_ranges:
            min_price, max_price = budget_ranges[budget_range]
            filters["min_price"] = min_price
            if max_price != float('inf'):
                filters["max_price"] = max_price
    
    return filters

def get_sort_options() -> dict:
    """Get available sort options"""
    return {
        "Newest": "newest",
        "Price: Low to High": "price_low",
        "Price: High to Low": "price_high"
    }
