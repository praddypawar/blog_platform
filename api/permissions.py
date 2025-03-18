from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only admins to modify categories.
    Authenticated users can view them.
    """

    def has_permission(self, request, view):
        # Allow GET requests for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only allow admins to create, update, or delete
        return request.user.is_authenticated and request.user.is_staff
    

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors to edit their own posts.
    """
    # def has_object_permission(self, request, view, obj):
    #     # Read permissions are allowed to any request
    #     if request.method in permissions.SAFE_METHODS:
    #         return True
            
    #     # Write permissions are only allowed to the author of the post
    #     return obj.author == request.user

    def has_permission(self, request, view):
        # Allow anyone to retrieve, like, comment, and view stats
        if view.action in ['retrieve', 'like', 'comment', 'stats']:
            return True

        # Ensure user is authenticated
        if not request.user.is_authenticated:
            return False

        # Ensure the user has a profile
        if not hasattr(request.user, 'profile'):
            return False

        # Allow only authors to create/update posts
        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.profile.role == 'author'
        
        return True

    def has_object_permission(self, request, view, obj):
        # Allow safe methods (GET) for everyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Only the post author can edit/delete their post
        return obj.author == request.user

class IsAuthor(permissions.BasePermission):
    """
    Custom permission to only allow users with 'author' role.
    """
    def has_permission(self, request, view):
        # Check if user has author role
        return (
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and 
            request.user.profile.role == 'author'
        )


class IsReader(permissions.BasePermission):
    """
    Custom permission to only allow users with 'reader' role.
    """
    def has_permission(self, request, view):
        # Check if user has reader role
        return (
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and 
            request.user.profile.role == 'reader'
        )


class IsCommentAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors to edit their own comments.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Write permissions are only allowed to the author of the comment
        return obj.author == request.user