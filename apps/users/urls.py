from django.urls import path
from .views import GoogleOAuthSignInView, SendConfirmationCodeView, VerifyConfirmationCodeView

urlpatterns = [
    path('auth/google/', GoogleOAuthSignInView.as_view(), name='google-auth'),
    path('code/send/', SendConfirmationCodeView.as_view(), name='send-code'),
    path('code/verify/', VerifyConfirmationCodeView.as_view(), name='verify-code'),
]
