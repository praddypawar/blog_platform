from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.utils import IntegrityError

from api.models import UserProfile, Category, Post, Comment, Like, PostView, PostStatistics


class UserProfileModelTests(TestCase):
    """
    Tests for the UserProfile model
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
    
    def test_profile_creation(self):
        """Test creating a user profile"""
        profile = UserProfile.objects.create(
            user=self.user,
            role='author',
            bio='Test bio'
        )
        self.assertEqual(profile.user.username, 'testuser')
        self.assertEqual(profile.role, 'author')
        self.assertEqual(profile.bio, 'Test bio')
    
    def test_profile_str_representation(self):
        """Test string representation of UserProfile"""
        profile = UserProfile.objects.create(
            user=self.user,
            role='author'
        )
        self.assertEqual(str(profile), 'testuser - author')
    
    def test_default_role(self):
        """Test default role is 'reader'"""
        profile = UserProfile.objects.create(user=self.user)
        self.assertEqual(profile.role, 'reader')


class CategoryModelTests(TestCase):
    """
    Tests for the Category model
    """
    def test_category_creation(self):
        """Test creating a category"""
        category = Category.objects.create(
            name='Technology',
            slug='technology',
            description='Tech articles'
        )
        self.assertEqual(category.name, 'Technology')
        self.assertEqual(category.slug, 'technology')
        self.assertEqual(category.description, 'Tech articles')
    
    def test_category_str_representation(self):
        """Test string representation of Category"""
        category = Category.objects.create(
            name='Technology',
            slug='technology'
        )
        self.assertEqual(str(category), 'Technology')
    
    def test_unique_slug(self):
        """Test that category slugs are unique"""
        Category.objects.create(name='Technology', slug='tech')
        with self.assertRaises(IntegrityError):
            Category.objects.create(name='Tech', slug='tech')


class PostModelTests(TestCase):
    """
    Tests for the Post model
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='author',
            email='author@example.com',
            password='password123'
        )
        self.category = Category.objects.create(
            name='Technology',
            slug='technology'
        )
    
    def test_post_creation(self):
        """Test creating a post"""
        post = Post.objects.create(
            title='Test Post',
            content='This is a test post',
            author=self.user,
            is_published=True
        )
        post.categories.add(self.category)
        
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.content, 'This is a test post')
        self.assertEqual(post.author.username, 'author')
        self.assertTrue(post.is_published)
        self.assertEqual(post.categories.count(), 1)
        self.assertEqual(post.categories.first().name, 'Technology')
    
    def test_post_str_representation(self):
        """Test string representation of Post"""
        post = Post.objects.create(
            title='Test Post',
            content='Content',
            author=self.user
        )
        self.assertEqual(str(post), 'Test Post')
    
    def test_post_ordering(self):
        """Test posts are ordered by created_at descending"""
        Post.objects.create(
            title='First Post',
            content='Content',
            author=self.user
        )
        Post.objects.create(
            title='Second Post',
            content='Content',
            author=self.user
        )
        
        posts = Post.objects.all()
        self.assertEqual(posts[0].title, 'Second Post')
        self.assertEqual