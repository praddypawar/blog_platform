from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile, Category, Post, Comment, Like, PostView, PostStatistics


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=UserProfile.USER_ROLES, default='reader')

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'role', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        role = validated_data.pop('role')
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        
        # Create user profile with role
        UserProfile.objects.create(user=user, role=role)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'role', 'bio', 'created_at')
        read_only_fields = ('created_at',)


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for categories"""
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments"""
    author_username = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = Comment
        fields = ('id', 'content', 'author', 'author_username', 'created_at', 'updated_at')
        read_only_fields = ('author', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        # Set the author to the current user
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    """Serializer for posts"""
    author_username = serializers.CharField(source='author.username', read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source='categories'
    )
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    views_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = (
            'id', 'title', 'content', 'author', 'author_username', 
            'categories', 'category_ids', 'created_at', 'updated_at',
            'is_published', 'comments_count', 'likes_count', 'views_count'
        )
        read_only_fields = ('author', 'created_at', 'updated_at', 'comments_count', 'likes_count', 'views_count')
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_views_count(self, obj):
        return obj.views.count()
    
    def create(self, validated_data):
        # Set the author to the current user
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PostDetailSerializer(PostSerializer):
    """Detailed serializer for post with comments"""
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ('comments',)


class LikeSerializer(serializers.ModelSerializer):
    """Serializer for post likes"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Like
        fields = ('id', 'post', 'user', 'user_username', 'created_at')
        read_only_fields = ('user', 'created_at')


class PostStatisticsSerializer(serializers.ModelSerializer):
    """Serializer for post statistics"""
    post_title = serializers.CharField(source='post.title', read_only=True)
    
    class Meta:
        model = PostStatistics
        fields = ('id', 'post', 'post_title', 'date', 'view_count', 'like_count', 'comment_count')
        read_only_fields = ('date', 'view_count', 'like_count', 'comment_count')