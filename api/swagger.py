from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView

# Add security definitions to Swagger
security_definitions = {
    'Bearer': {
        'type': 'apiKey',
        'name': 'Authorization',
        'in': 'header'
    }
}

class TokenObtainPairViewExtended(TokenObtainPairView):
    """
    Takes a set of user credentials and returns JWT access and refresh tokens
    """
    @swagger_auto_schema(
        operation_description="Takes a set of user credentials and returns JWT access and refresh tokens",
        responses={
            '200': 'Returns access and refresh tokens',
            '401': 'Invalid credentials'
        },
        security=[]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)