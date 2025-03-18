from celery import shared_task
from django.core.mail import send_mail
from django.db.models import Count
from django.utils import timezone
from django.conf import settings
import logging
from datetime import timedelta

from .models import User, Post, PostStatistics

logger = logging.getLogger(__name__)


@shared_task
def send_welcome_email(user_id):
    """
    Send a welcome email to newly registered users
    """
    try:
        user = User.objects.get(id=user_id)
        send_mail(
            subject='Welcome to Blog Platform!',
            message=f'Hi {user.username}, welcome to our Blog Platform! Start exploring posts or create your own.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        logger.info(f"Welcome email sent to {user.email}")
    except User.DoesNotExist:
        logger.error(f"Cannot send welcome email: User with id {user_id} does not exist")
    except Exception as e:
        logger.error(f"Failed to send welcome email: {str(e)}")


@shared_task
def generate_daily_post_statistics():
    """
    Generate daily statistics for all posts
    """
    try:
        # Get yesterday's date
        yesterday = timezone.now().date() - timedelta(days=1)
        
        # Get all posts
        posts = Post.objects.all()
        
        for post in posts:
            # Count views, likes, and comments for the post on the specified date
            view_count = post.views.filter().count()
            like_count = post.likes.filter(created_at__date=yesterday).count()
            comment_count = post.comments.filter(created_at__date=yesterday).count()
            
            # Create or update statistics for the post
            PostStatistics.objects.update_or_create(
                post=post,
                date=yesterday,
                defaults={
                    'view_count': view_count,
                    'like_count': like_count,
                    'comment_count': comment_count,
                }
            )
        
        logger.info(f"Daily statistics generated for {posts.count()} posts")
    except Exception as e:
        logger.error(f"Failed to generate daily statistics: {str(e)}")


@shared_task
def clean_old_view_data(days=30):
    """
    Clean old view data to prevent database bloat
    """
    try:
        cutoff_date = timezone.now() - timedelta(days=days)
        from .models import PostView
        
        # Delete old view records
        deleted_count, _ = PostView.objects.filter(timestamp__lt=cutoff_date).delete()
        
        logger.info(f"Cleaned up {deleted_count} old view records older than {days} days")
    except Exception as e:
        logger.error(f"Failed to clean old view data: {str(e)}")