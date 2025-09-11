from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from .models import User

class RegisterView(APIView):
    def post(self, request):
        """Register a new user"""
        try:
            data = request.data
            
            # Check if user already exists
            if User.objects.filter(username=data['username']).exists():
                return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Create Django auth user
            user = User.objects.create_user(
                username=data['username'],
                email=data.get('email', ''),
                password=data['password'],
                first_name=data.get('first_name', ''),
                last_name=data.get('last_name', ''),
            )
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        """Login a user and return JWT tokens"""
        try:
            data = request.data
            username = data.get('username')
            password = data.get('password')
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                refresh = RefreshToken.for_user(user)
                
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                return Response({
                    'error': 'Invalid username or password'
                }, status=status.HTTP_401_UNAUTHORIZED)
                
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get information about the current logged-in user"""
        try:
            user = request.user
            return Response(UserSerializer(user).data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Logout by blacklisting the provided refresh token"""
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({'error': 'refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                token = RefreshToken(refresh_token)
            except TokenError as te:
                return Response({'error': str(te)}, status=status.HTTP_400_BAD_REQUEST)

            # Ensure the token belongs to the authenticated user
            if str(request.user.id) != str(token.get('user_id')):
                return Response({'error': 'token does not belong to the current user'}, status=status.HTTP_403_FORBIDDEN)

            token.blacklist()
            return Response({'detail': 'Logged out'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LogoutAllView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Logout from all sessions by blacklisting all refresh tokens for the user"""
        try:
            # Issue a new refresh token and blacklist all outstanding tokens for this user
            # SimpleJWT provides a helper to blacklist via OutstandingToken/BlacklistedToken models
            from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

            tokens = OutstandingToken.objects.filter(user=request.user)
            for t in tokens:
                BlacklistedToken.objects.get_or_create(token=t)
            return Response({'detail': 'Logged out from all sessions'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
