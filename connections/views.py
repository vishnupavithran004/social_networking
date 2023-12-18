# Create your views here.
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework import pagination, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.viewsets import ModelViewSet

from connections.models import FriendRequest
from connections.serializers import FriendRequestListSerializer
from users.models import User


class ConnectionViewSet(ModelViewSet):
    """
    ModelViewSet for creating and listing Users
    """
    queryset = FriendRequest.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = pagination.PageNumberPagination
    throttle_scope = 'send_request'

    def get_user_by_id(self, user_id):
        try:
            user = User.objects.get(id=user_id)
            return user
        except User.DoesNotExist:
            return None

    def create(self, request, *args, **kwargs):

        message = 'Friend request successfully sent!'
        response_status = status.HTTP_201_CREATED
        user = self.get_user_by_id(request.data.get('user_id'))
        if not user:
            data = {'message': 'Invalid User!'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        requested_by = request.user
        try:
            FriendRequest.objects.create(user=user, friend=requested_by)
        except IntegrityError:
            message = 'Friend request has been already sent to this user!'
            response_status = status.HTTP_400_BAD_REQUEST
        return Response({'message': message}, status=response_status)

    def list(self, request, *args, **kwargs):
        """
        Return list of friend requests received
        """
        queryset = self.queryset.filter(
            user=request.user, status=FriendRequest.RECEIVED)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = FriendRequestListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = FriendRequestListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_throttles(self):
        if self.action == 'create':
            throttle_classes = [ScopedRateThrottle]
        else:
            throttle_classes = []  # No throttle for other actions
        return [throttle() for throttle in throttle_classes]


class FriendsViewset(ModelViewSet):
    """
    ViewSet for Managing Friends.
    """
    permission_classes = [IsAuthenticated]
    pagination_class = pagination.PageNumberPagination
    queryset = FriendRequest.objects.filter(status=FriendRequest.ACCEPTED)

    def list(self, request, *args, **kwargs):
        """
        Method lists all the friends of the current user
        """
        queryset = self.queryset.filter(
            user=request.user, status=FriendRequest.ACCEPTED)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = FriendRequestListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = FriendRequestListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
        Method for updating the request status to accepted or rejected.
        """
        request_id = kwargs.get('pk')
        accepted = request.data.get('accepted')
        request_status = FriendRequest.ACCEPTED if accepted else FriendRequest.REJECTED
        try:
            friend_request = FriendRequest.objects.get(id=request_id)
            if friend_request.status != FriendRequest.RECEIVED:
                raise ValidationError()
            friend_request.status = request_status
            friend_request.save()
            response_data = {
                "message": f"{friend_request.get_status_display()} Successfully."
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception:
            error_data = {
                "message": "Invalid Friend Request"
            }
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)
