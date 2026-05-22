import random
import redis
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

redis_client = redis.StrictRedis(
    host=settings.REDIS_HOST, 
    port=settings.REDIS_PORT, 
    db=1, 
    decode_responses=True
)

class GoogleOAuthSignInView(APIView):
    def post(self, request):
        code = request.data.get('code')
        if not code:
            return Response({'error': 'Code is required'}, status=status.HTTP_400_BAD_REQUEST)

        token_url = "https://oauth2.googleapis.com/token"
        data = {
            'code': code,
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri': settings.GOOGLE_REDIRECT_URI,
            'grant_type': 'authorization_code',
        }
        
        token_response = requests.post(token_url, data=data)
        if token_response.status_code != 200:
            return Response({'error': 'Failed to get token from Google'}, status=token_response.status_code)
        
        token_data = token_response.json()
        access_token = token_data.get('access_token')

        user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        user_info_response = requests.get(user_info_url, headers={'Authorization': f'Bearer {access_token}'})
        
        if user_info_response.status_code != 200:
            return Response({'error': 'Failed to get user info from Google'}, status=user_info_response.status_code)

        user_info = user_info_response.json()
        email = user_info.get('email')
        given_name = user_info.get('given_name', '')
        family_name = user_info.get('family_name', '')

        if not email:
            return Response({'error': 'Email not provided by Google'}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(email=email, defaults={
            'username': email.split('@')[0],
            'first_name': given_name,
            'last_name': family_name,
            'registration_source': 'google',
            'is_active': True
        })

        if not created:
            user.first_name = given_name
            user.last_name = family_name
            user.is_active = True

        user.last_login = timezone.now()
        user.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'message': 'Successfully authenticated via Google'
        }, status=status.HTTP_200_OK)

class SendConfirmationCodeView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        code = str(random.randint(100000, 999999))
        redis_client.set(f"code:{email}", code, ex=300)
        return Response({'message': 'Code sent successfully'}, status=status.HTTP_200_OK)

class VerifyConfirmationCodeView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user_code = request.data.get('code')
        
        if not email or not user_code:
            return Response({'error': 'Email and code are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        saved_code = redis_client.get(f"code:{email}")
        
        if not saved_code:
            return Response({'error': 'Code expired or does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            
        if saved_code == str(user_code):
            redis_client.delete(f"code:{email}")
            return Response({'message': 'Code verified successfully!'}, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid code'}, status=status.HTTP_400_BAD_REQUEST)
