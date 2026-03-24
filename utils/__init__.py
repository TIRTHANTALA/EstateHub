"""
EstateHub Utilities Package
"""
from .styles import get_custom_css, inject_css
from .helpers import (
    format_price,
    format_date,
    time_ago,
    get_property_image_placeholder,
    show_success,
    show_error,
    show_info,
    show_warning,
    validate_email,
    validate_phone,
    truncate_text
)
from .filters import build_filter_query, get_sort_options
from .recommendations import (
    get_similar_properties,
    get_recommended_properties,
    suggest_price
)

__all__ = [
    'get_custom_css',
    'inject_css',
    'format_price',
    'format_date',
    'time_ago',
    'get_property_image_placeholder',
    'show_success',
    'show_error',
    'show_info',
    'show_warning',
    'validate_email',
    'validate_phone',
    'truncate_text',
    'build_filter_query',
    'get_sort_options',
    'get_similar_properties',
    'get_recommended_properties',
    'suggest_price'
]
