from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from users.models import User
from users.serializers import UserSerializer, LoginSerializer
from users.utils import get_tokens_for_user
from rest_framework import pagination


class UserModelViewSet(ModelViewSet):
    """
    ModelViewSet for creating and listing Users
    """
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=True, is_staff=False)
    pagination_class = pagination.PageNumberPagination
    http_method_names = ['get', 'post', 'head']

    def get_permissions(self):
        if self.action in ('create', 'login'):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        """
        Returns list of users by filtering the queryset using query param.
        """
        filter_param = request.query_params.get('filter_param')
        queryset = self.queryset
        if filter_param:
            queryset = self.queryset.filter(
                email__iexact=filter_param).exclude(user=request.user)
            if queryset:
                return queryset
            queryset = self.queryset.filter(name__icontains=filter_param)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_name='login', name='login')
    def login(self, request, *args, **kwargs):
        """
        Returns Access token if login credentials are valid.
        """
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            user = authenticate(
                request=self.request,
                email=serializer.validated_data.get('email'),
                password=serializer.validated_data.get('password')
            )
            if user:
                reponse_data = get_tokens_for_user(user)
                message = "Login Successful"
                reponse_data.update({'message': message})
                response = Response(
                    data=reponse_data, status=status.HTTP_200_OK)
                return response
            errors = "Invalid Email or Password!"
        else:
            errors = serializer.errors
        response_data = {
            'errors': errors
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        response_data = {
            "message": "User created successfully."
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
