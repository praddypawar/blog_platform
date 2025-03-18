import logging
import time
import json
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware for logging requests and response information
    """
    
    def process_request(self, request):
        """
        Process and log incoming request information
        """
        request.start_time = time.time()
        
        # Extract and sanitize headers (remove sensitive information)
        headers = {}
        for header, value in request.META.items():
            if header.startswith('HTTP_'):
                name = header[5:].lower().replace('_', '-')
                # Skip logging authorization headers in detail
                if name == 'authorization':
                    headers[name] = 'JWT Token Present' if value else 'No Token'
                else:
                    headers[name] = value
        
        # Log the request
        logger.info(
            f"Request: {request.method} {request.path} - "
            f"USER: {request.user if request.user.is_authenticated else 'Anonymous'} - "
            f"IP: {self.get_client_ip(request)}"
        )
        
        # For debugging, log more details at debug level
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(
                f"Request Details: {request.method} {request.path} - "
                f"Query Params: {json.dumps(dict(request.GET))} - "
                f"Headers: {json.dumps(headers)}"
            )
        
        return None
    
    def process_response(self, request, response):
        """
        Process and log outgoing response information
        """
        # Calculate request processing time
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            
            # Log the response
            logger.info(
                f"Response: {request.method} {request.path} - "
                f"Status: {response.status_code} - "
                f"Duration: {duration:.2f}s"
            )
            
            # Add processing time header
            response['X-Processing-Time'] = f"{duration:.2f}s"
        
        return response
    
    def get_client_ip(self, request):
        """
        Extract the client IP address from the request
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip