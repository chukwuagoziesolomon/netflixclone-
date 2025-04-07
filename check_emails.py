import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'netflixcloneproject.settings')
django.setup()

from django.contrib.auth.models import User

# Get all users
users = User.objects.all()

print("All users in the database:")
for user in users:
    print(f"Username: {user.username}, Email: {user.email}")

# Check specific emails
email1 = "chukwuagoziesolomon@gmail.com"
email2 = "chukwuagoziesolomon1@gmail.com"

user1 = User.objects.filter(email=email1).first()
user2 = User.objects.filter(email=email2).first()

print(f"\nChecking specific emails:")
print(f"Email '{email1}' exists: {user1 is not None}")
print(f"Email '{email2}' exists: {user2 is not None}")

# Check for similar emails
print("\nChecking for similar emails:")
for user in users:
    if "chukwuagoziesolomon" in user.email:
        print(f"Found similar email: {user.email}") 