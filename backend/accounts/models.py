from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import uuid

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    
class User(AbstractUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, db_index=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    
    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return self.email    
    
class Profile(models.Model):
    GENDER_CHOICES = [
        ('female', 'Feminino'),
        ('male', 'Masculino'),
        ('other', 'Outro')
    ]
    
    SIZE_CHOICES = [
        ('S', 'Pequeno'),
        ('M', 'Médio'),
        ('L', 'Grande'),
        ('XL', 'Extra Grande'),
        ('XXL', 'Extra Extra Grande')
    ]
    
    SIZE_SYSTEM_CHOICES = [
        ('US', 'Estados Unidos'),
        ('EU', 'Europa'),
        ('UK', 'Reino Unido'),
        ('JP', 'Japão'),
        ('BR', 'Brasil')
    ]
    
    CURRENCY_CHOICES = [
        ('USD', 'Dólar Americano'),
        ('EUR', 'Euro'),
        ('GBP', 'Libra Esterlina'),
        ('JPY', 'Iene Japonês'),
        ('BRL', 'Real Brasileiro')
    ]
    
    LANGUAGE_CHOICES = [
        ('en', 'Inglês'),
        ('pt', 'Português'),
        ('es', 'Espanhol'),
        ('fr', 'Francês'),
        ('de', 'Alemão')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, default='')
    gender = models.CharField(max_length=10, blank=True, null=True, choices=GENDER_CHOICES)
    preferred_size = models.CharField(max_length=3, blank=True, null=True, choices=SIZE_CHOICES)
    size_system = models.CharField(max_length=3, blank=True, default='US', choices=SIZE_SYSTEM_CHOICES)
    language = models.CharField(max_length=2, blank=True, default='pt', choices=LANGUAGE_CHOICES)
    currency = models.CharField(max_length=3, blank=True, default='BRL', choices=CURRENCY_CHOICES)
    country = models.CharField(max_length=100, blank=True, default='Brasil')
    style_preferences = models.JSONField(blank=True, default=dict)
    fcm_token = models.CharField(max_length=255, blank=True, null=True)
    height_cm = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'profiles'

    def __str__(self):
        return f"perfil de {self.user.email}"
        
class Address(models.Model):
    ADDRESS_TYPE_CHOICES = [
        ('home', 'Residencial'),
        ('work', 'Comercial'),
        ('other', 'Outro')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=10, blank=True, null=True, choices=ADDRESS_TYPE_CHOICES, default='home')
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    street = models.CharField(max_length=255)
    district = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default='Brasil')
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'addresses'
        verbose_name_plural = 'Addresses'
        Indexes = [
            models.Index(fields=['user', 'is_default']),
        ]
        
    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.country}"