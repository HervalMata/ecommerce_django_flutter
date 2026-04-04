from rest_framework import serializers
from .models import User, Profile, Address

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'date_joined']
        read_only_fields = ['id', 'date_joined']
        
class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8, max_length=128)
    phone = serializers.CharField(required=False, allow_blank=True)
        
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Um usuário com esse email já existe.")
        return value

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)      
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'avatar', 'gender', 'preferred_size', 'style_preferences', 'height_cm', 'weight_kg', 'size_system', 'language', 'currency', 'country', 'created_at', 'updated_at', 'name']
        read_only_fields = ['user', 'created_at', 'updated_at' ]
        
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'user', 'address_type', 'full_name', 'phone', 'street', 'district', 'city', 'state', 'postal_code', 'country', 'is_default', 'created_at', 'updated_at']
        read_only_fields = ['id','user', 'created_at', 'updated_at']           