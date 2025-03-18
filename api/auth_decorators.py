from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

token_param = openapi.Parameter(
    'Authorization',
    openapi.IN_HEADER,
    description="JWT Token in format: Bearer <token>",
    type=openapi.TYPE_STRING
)

def token_required(view_func):
    """
    Decorator to mark views as requiring token authentication
    """
    return swagger_auto_schema(
        manual_parameters=[token_param],
        security=[{'Bearer': []}],
    )(view_func)