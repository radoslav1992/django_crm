"""File upload validators for security"""
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions


def validate_image_file(file):
    """Validate uploaded image files"""
    # Check file size (max 5MB)
    if file.size > 5 * 1024 * 1024:
        raise ValidationError('Image file too large ( > 5MB )')
    
    # Check file extension
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    ext = file.name.lower().split('.')[-1] if '.' in file.name else ''
    if f'.{ext}' not in allowed_extensions:
        raise ValidationError(f'Unsupported file type. Allowed: {", ".join(allowed_extensions)}')
    
    # Check image dimensions (if it's an image)
    try:
        w, h = get_image_dimensions(file)
        if w and h and (w > 4000 or h > 4000):
            raise ValidationError('Image dimensions too large (max 4000x4000)')
    except Exception:
        # If we can't get dimensions, it might not be a valid image
        raise ValidationError('Invalid image file')


def validate_document_file(file):
    """Validate uploaded document files"""
    # Check file size (max 10MB)
    if file.size > 10 * 1024 * 1024:
        raise ValidationError('File too large ( > 10MB )')
    
    # Check file extension
    allowed_extensions = ['.pdf', '.doc', '.docx', '.txt']
    ext = file.name.lower().split('.')[-1] if '.' in file.name else ''
    if f'.{ext}' not in allowed_extensions:
        raise ValidationError(f'Unsupported file type. Allowed: {", ".join(allowed_extensions)}')


def validate_avatar(file):
    """Validate avatar uploads"""
    # Check file size (max 2MB for avatars)
    if file.size > 2 * 1024 * 1024:
        raise ValidationError('Avatar too large ( > 2MB )')
    
    # Check file extension
    allowed_extensions = ['.jpg', '.jpeg', '.png']
    ext = file.name.lower().split('.')[-1] if '.' in file.name else ''
    if f'.{ext}' not in allowed_extensions:
        raise ValidationError(f'Unsupported file type. Allowed: {", ".join(allowed_extensions)}')
    
    # Check image dimensions
    try:
        w, h = get_image_dimensions(file)
        if w and h and (w > 1000 or h > 1000):
            raise ValidationError('Avatar dimensions too large (max 1000x1000)')
    except Exception:
        raise ValidationError('Invalid image file')

