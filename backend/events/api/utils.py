# events/api/utils.py
from rest_framework.response import Response
from rest_framework import status
from typing import Any, Optional

def error_response(
    message: str, 
    status_code: int = status.HTTP_400_BAD_REQUEST,
    error_code: Optional[str] = None
) -> Response:
    """
    Standardized error response format
    """
    error_data = {
        'message': str(message),
        'status_code': status_code
    }
    
    if error_code:
        error_data['error_code'] = error_code
        
    return Response(
        {
            'success': False,
            'error': error_data
        },
        status=status_code,
        content_type='application/json'  # Explicitly set content type
    )

def success_response(
    data: Any = None, 
    status_code: int = status.HTTP_200_OK,
    message: Optional[str] = None
) -> Response:
    """
    Standardized success response format
    """
    response_data = {
        'success': True
    }
    
    if data is not None:
        response_data['data'] = data
        
    if message:
        response_data['message'] = message
        
    return Response(
        response_data, 
        status=status_code,
        content_type='application/json'  # Explicitly set content type
    )