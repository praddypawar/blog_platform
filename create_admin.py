import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_platform.settings')
django.setup()

# Import models
from django.contrib.auth.models import User
from api.models import UserProfile

# Create superuser if not exists
if not User.objects.filter(username='admin').exists():
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123'
    )
    UserProfile.objects.create(user=admin_user, role='author')
    print("Superuser created successfully!")
else:
    admin_user = User.objects.get(username='admin')
    admin_user.set_password('adminpass123')
    admin_user.save()
    print("Superuser password reset to 'adminpass123'")

print("\nAdmin credentials:")
print("Username: admin")
print("Password: adminpass123")
print("\nYou can now login at: http://localhost:8000/api/auth/login/")