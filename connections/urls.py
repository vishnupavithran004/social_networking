from django.urls import path, include
from rest_framework import routers

from connections.views import ConnectionViewSet, FriendsViewset

router = routers.DefaultRouter()

router.register(
    r'friend_request', ConnectionViewSet, basename='requests'
)
router.register(
    r'manage_friends', FriendsViewset, basename='friends'
)

urlpatterns = [
    path('', include(router.urls)),
]
