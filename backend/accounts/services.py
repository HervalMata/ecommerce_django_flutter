from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from .models import User, Profile, Address

class AccountService:
    @staticmethod
    @transaction.atomic
    def create_user(email, password, phone=None):
        try:
            # Create user
            user = User.objects.create_user(
            email=email,
            password=password,
            phone=phone
        )
        except IntegrityError:
            raise ValidationError("A user with this email already exists.")
        
        
        # Create profile if profile data is provided
        Profile.objects.get_or_create(user=user)
        
        return user
    
    @staticmethod
    def update_fcm_token(user, fcm_token):
        profile = user.profile
        profile.fcm_token = fcm_token
        profile.save(update_fields=["fcm_token"])
        return profile
    
    @staticmethod
    def get_user_addresses(user):
        return Address.objects.filter(user=user).order_by('is_default', '-created_at')
    
    @staticmethod
    def create_address(user, **kwargs):
        address = Address.objects.create(user=user, **kwargs)
        return address
    
    @staticmethod
    def get_address(user, address_id):
        try:
            return Address.objects.get(user=user, id=address_id)
        except Address.DoesNotExist:
            raise ValidationError("Address not found.")
        
    @staticmethod
    @transaction.atomic
    def update_address(user, address_id, **kwargs):
        address = Address.objects.get(user=user, id=address_id)
        for key, value in kwargs.items():
            if hasattr(address, key):
                setattr(address, key, value)
        address.save()
        return address    
    
    @staticmethod
    def delete_address(user, address_id):
        address = Address.objects.get(user=user, id=address_id)
        address.delete()
        
    @staticmethod
    @transaction.atomic
    def set_default_address(user, address_id):
        address = Address.objects.get(user=user, id=address_id)
        Address.objects.filter(user=user, is_default=True).update(is_default=False)
        address.is_default = True
        address.save(update_fields=['is_default'])
        return address    