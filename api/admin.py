from django.contrib import admin
from .models import (
    UserProfile, Category, Post, Comment, 
    Like, PostView, PostStatistics
)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('user__username', 'user__email', 'bio')
    date_hierarchy = 'created_at'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class LikeInline(admin.TabularInline):
    model = Like
    extra = 0


class PostViewInline(admin.TabularInline):
    model = PostView
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_published')
    list_filter = ('is_published', 'created_at', 'categories')
    search_fields = ('title', 'content', 'author__username')
    date_hierarchy = 'created_at'
    filter_horizontal = ('categories',)
    inlines = [CommentInline, LikeInline, PostViewInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username', 'post__title')
    date_hierarchy = 'created_at'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'post__title')
    date_hierarchy = 'created_at'


@admin.register(PostView)
class PostViewAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'ip_address', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('user__username', 'post__title', 'ip_address')
    date_hierarchy = 'timestamp'


@admin.register(PostStatistics)
class PostStatisticsAdmin(admin.ModelAdmin):
    list_display = ('post', 'date', 'view_count', 'like_count', 'comment_count')
    list_filter = ('date',)
    search_fields = ('post__title',)
    date_hierarchy = 'date'