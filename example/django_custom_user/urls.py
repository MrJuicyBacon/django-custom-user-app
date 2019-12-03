from django.urls import path, include

urlpatterns = [
    path('', include('django_custom_user_app.urls'))
]
