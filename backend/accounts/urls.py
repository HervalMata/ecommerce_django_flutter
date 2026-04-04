from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', views.profile_view, name='profile'),
    path('fcm_token/', views.fcm_token, name='update_fcm_token'),
    path('addresses/', views.addresses, name='addresses'),
    path('addresses/<uuid:address_id>/', views.address_detail, name='address_detail'),
    path('addresses/<uuid:address_id>/set-default/', views.set_default_address, name='set_default_address'),

]
