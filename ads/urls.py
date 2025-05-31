from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('create/', CreateAdView.as_view(), name='create-ad'),
    path('delete/', DeleteAdView.as_view(), name='delete-ad'),
    path('edit/', EditAdView.as_view(), name='edit-ad')
]
