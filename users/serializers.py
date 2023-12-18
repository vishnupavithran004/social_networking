from rest_framework import serializers

from users.models import User
from secrets import compare_digest


class UserSerializer(serializers.ModelSerializer):
    """
    User model Serializer
    """
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'name', 'password', 'confirm_password', 'id')
        extra_kwargs = {
            'password': {'write_only': True},
        }
        read_only_fields = ('id', )

    @staticmethod
    def validate_email(email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "User with this Email already exists!.")
        return email

    def validate(self, data):
        breakpoint()
        confirm_password = data.get('confirm_password')
        password = data.get('password')
        if not compare_digest(password, confirm_password):
            raise serializers.ValidationError(
                "Password and Confirm Password does not match")
        return data

    def create(self, data):
        breakpoint()
        data.pop('confirm_password')
        password = data.pop('password')
        user = User(**data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """
    User login serializer
    """
    email = serializers.EmailField(
        error_messages={"required": "Valid email required!",
                        "invalid": "Valid email required!"
                        })
    password = serializers.CharField(
        error_messages={"required": "Password required!"})
