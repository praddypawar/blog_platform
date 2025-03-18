from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    UserRegistrationView, UserProfileViewSet, CategoryViewSet,
    PostViewSet, CommentViewSet
)
from .swagger import TokenObtainPairViewExtended

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    # JWT auth endpoints
    path('auth/login/', TokenObtainPairViewExtended.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', UserRegistrationView.as_view(), name='user_registration'),
    
    # Include router URLs
    path('', include(router.urls)),
]