from django.db import transaction
from django.core.exceptions import ValidationError
from .models import User, Profile, Address

class AccountService:
    @staticmethod
    @transaction.atomic
    def create_user(email, password, phone=None):
        # Validate user data
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        
        # Create user
        user = User.objects.create_user(
            email=email,
            password=password,
            phone=phone
        )
        
        # Create profile if profile data is provided
        Profile.objects.get_or_create(user=user)
        
        return user
    
    @staticmethod
    def update_fcm_token(user, fcm_token):
        profile = user.profile
        profile.fcm_token = fcm_token
        profile.save(update_fields=["fcm_token"])
        return profile