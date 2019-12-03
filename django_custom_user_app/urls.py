from django.urls import path
from .views import auth, profile

urlpatterns = [
    path('api/auth/', auth, name='auth'),
    path('api/profiles/<str:user_id>', profile, name='profile')
]
