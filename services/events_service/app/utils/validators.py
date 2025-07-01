from app.utils.exceptions import ValidationError
from app.config import config

def validate_event_data(data):
    """Validate event creation data"""
    if not data:
        raise ValidationError("Request body is required")
    
    required_fields = ['name', 'description', 'short_description', 'organizer_id', 'location', 'start_time', 'end_time', 'category', 'image_url', 'capacity', 'is_public', 'is_virtual', 'is_recurring', 'is_free', 'virtual_meeting_link', 'tags', 'status', 'fee']

    for field in required_fields:
        if field not in data:
            raise ValidationError(f"Missing required field: {field}")
        if not data[field]:
            raise ValidationError(f"Field {field} cannot be empty")

    
    # Validate string lengths
    if len(data['name']) > 200:
        raise ValidationError("Event name too long (max 200 characters)")
    if len(data['description']) > 1000:
        raise ValidationError("Description too long (max 1000 characters)")
    if len(data['short_description']) > 500:
        raise ValidationError("Short description too long (max 500 characters)")
    if len(data['location']) > 500:
        raise ValidationError("Location too long (max 500 characters)")

def validate_search_params(args):
    """Validate search parameters"""
    params = {}
    
    # Text query
    if 'query' in args:
        params['query'] = args.get('query').strip()
    
    # Category filter
    if 'category' in args:
        params['category'] = args.get('category').strip()
    
    # Pagination
    try:
        params['page'] = int(args.get('page', 1))
        if params['page'] < 1:
            raise ValidationError("page must be positive")
    except (ValueError, TypeError):
        raise ValidationError("page must be a valid integer")
    
    try:
        params['size'] = int(args.get('size', config.DEFAULT_PAGE_SIZE))
        if params['size'] < 1:
            raise ValidationError("size must be positive")
        if params['size'] > config.MAX_PAGE_SIZE:
            raise ValidationError(f"size cannot exceed {config.MAX_PAGE_SIZE}")
    except (ValueError, TypeError):
        raise ValidationError("size must be a valid integer")
    
    return params

