from rest_framework import viewsets, generics, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema

from .models import User, UserProfile, Category, Post, Comment, Like, PostView, PostStatistics
from .serializers import (
    UserRegistrationSerializer, UserProfileSerializer, CategorySerializer,
    PostSerializer, PostDetailSerializer, CommentSerializer, LikeSerializer,
    PostStatisticsSerializer
)
from .permissions import IsAuthor, IsAuthorOrReadOnly, IsCommentAuthorOrReadOnly,IsAdminOrReadOnly
from .tasks import send_welcome_email


class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for user registration
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Trigger welcome email
        send_welcome_email.delay(user.id)
        
        return Response({
            "message": "User registered successfully",
            "user": UserProfileSerializer(user.profile).data
        }, status=status.HTTP_201_CREATED)


class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing user profiles
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Get the current user's profile
        """
        serializer = self.get_serializer(request.user.profile)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing categories
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing blog posts
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'categories', 'is_published']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Filter posts based on search parameters
        """
        queryset = Post.objects.all()
        
        # Search by title or content
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(content__icontains=search_query)
            )
        
        # Filter by author
        author = self.request.query_params.get('author', None)
        if author:
            queryset = queryset.filter(author__username=author)
            
        # Filter by date
        date = self.request.query_params.get('date', None)
        if date:
            queryset = queryset.filter(created_at__date=date)
            
        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(categories__slug=category)
            
        # Sort by popularity (view count)
        sort_by = self.request.query_params.get('sort_by', None)
        if sort_by == 'popularity':
            # Count views for each post and order by that count
            queryset = queryset.annotate(view_count=models.Count('views')).order_by('-view_count')
            
        return queryset
    
    def get_serializer_class(self):
        """
        Return different serializers for list and detail views
        """
        if self.action == 'retrieve':
            return PostDetailSerializer
        return PostSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """
        Override retrieve to track post views
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        # Track the view
        PostView.objects.create(
            post=instance,
            user=request.user if request.user.is_authenticated else None,
            ip_address=self.get_client_ip(request)
        )
        
        return Response(serializer.data)
    
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
    
    @action(detail=True, methods=['post'],permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        """
        Like or unlike a post
        """
        post = self.get_object()
        user = request.user
        
        # Check if the user already liked the post
        like_exists = Like.objects.filter(post=post, user=user).exists()
        
        if like_exists:
            # Unlike the post
            Like.objects.filter(post=post, user=user).delete()
            return Response({"message": "Post unliked successfully"}, status=status.HTTP_200_OK)
        else:
            # Like the post
            like = Like.objects.create(post=post, user=user)
            serializer = LikeSerializer(like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'],permission_classes=[IsAuthenticated])
    def comment(self, request, pk=None):
        """
        Add a comment to a post
        """
        post = self.get_object()
        serializer = CommentSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save(post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """
        Get statistics for a post
        """
        post = self.get_object()
        
        # Get the latest statistics
        try:
            latest_stats = PostStatistics.objects.filter(post=post).latest('date')
            serializer = PostStatisticsSerializer(latest_stats)
            return Response(serializer.data)
        except PostStatistics.DoesNotExist:
            # If no statistics exist, return current counts
            stats = {
                'post': post.id,
                'post_title': post.title,
                'date': timezone.now().date(),
                'view_count': post.views.count(),
                'like_count': post.likes.count(),
                'comment_count': post.comments.count(),
            }
            return Response(stats)


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing comments
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentAuthorOrReadOnly]
    
    def get_queryset(self):
        """
        Filter comments by post if post_id is provided
        """
        queryset = Comment.objects.all()
        post_id = self.request.query_params.get('post_id', None)
        
        if post_id:
            queryset = queryset.filter(post__id=post_id)
            
        return queryset
    
    @swagger_auto_schema(auto_schema=None)  # Hides POST from Swagger
    def create(self, request, *args, **kwargs):
        """
        Disable the POST method completely
        """
        return Response(
            {"detail": "Creating comments is not allowed."}, 
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )