from django.conf import settings
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    """
    @param user: User object
    @return: token object
    """

    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
