from django.urls import path, include
from rest_framework import routers

from users.views import UserModelViewSet

router = routers.DefaultRouter()

router.register(
    r'api', UserModelViewSet, basename='api'
)

urlpatterns = [
    path('', include(router.urls)),
]
