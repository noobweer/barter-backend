from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('create-ad/', CreateAdView.as_view(), name='create-ad'),
    path('delete-ad/', DeleteAdView.as_view(), name='delete-ad'),
    path('edit-ad/', EditAdView.as_view(), name='edit-ad'),
    path('ads/', AdsView.as_view(), name='ads'),
    path('create-exchange/', CreateExchangeView.as_view(), name='create-exchange'),
    path('edit-exchange/', EditExchangeView.as_view(), name='edit-exchange'),
    path('exchanges/', ExchangesView.as_view(), name='exchanges')
]
