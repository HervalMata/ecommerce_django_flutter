from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Profile
from .serializers import UserSerializer, UserRegistrationSerializer, UserLoginSerializer, ProfileSerializer, AddressSerializer
from .services import AccountService
from django.core.exceptions import ValidationError

# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = AccountService.create_user(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                phone=serializer.validated_data.get('phone')
            )
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": UserSerializer(user).data,
            "tokens": {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(
            email=serializer.validated_data['email'], 
            password=serializer.validated_data['password']
        )
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": UserSerializer(user).data,
                "tokens": {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PATCH'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    profile = request.user.profile
    if request.method == 'GET':
        return Response(ProfileSerializer(profile, context={'request': request}).data)
    elif request.method == 'PATCH':
        serializer = ProfileSerializer(profile, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def fcm_token(request):
    fcm_token = request.data.get('fcm_token')
    if not fcm_token:
        return Response({"error": "FCM token is required."}, status=status.HTTP_400_BAD_REQUEST)
    AccountService.update_fcm_token(request.user, fcm_token)
    return Response({"detail": "FCM token updated successfully."}, status=status.HTTP_200_OK)    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def addresses(request):
    if request.method == 'GET':
        addresses = AccountService.get_user_addresses(request.user)
        return Response(AddressSerializer(addresses, many=True, context={'request': request}).data)
    elif request.method == 'POST':
        serializer = AddressSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            address = AccountService.create_address(request.user, **serializer.validated_data)
            return Response(AddressSerializer(address, context={'request': request}).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT','PATCH', 'DELETE'])
@permission_classes([IsAuthenticated]) 
def address_detail(request, address_id):
    try:
        if request.method == 'GET':
            address = AccountService.get_address(request.user, address_id)
            return Response(AddressSerializer(address).data)
        elif request.method in ['PUT', 'PATCH']:
            serializer = AddressSerializer(data= request.data, partial= (request.method == 'PATCH'))
            if serializer.is_valid():
                address = AccountService.update_address(request.user, address_id, **serializer.validated_data)
                serializer.save()
                return Response(AddressSerializer(address).data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            address = AccountService.get_address(request.user, address_id)
            address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_default_address(request, address_id):
    try:
        address = AccountService.set_default_address(request.user, address_id)
        return Response(AddressSerializer(address).data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
      