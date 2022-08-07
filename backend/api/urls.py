from django.urls import include
from django.urls import path, include
from api.api_views import *


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('user/', UserAPIView.as_view(), name='user'),
    path('allergy/', AllergyAPIView.as_view(), name='allergy'),
]
