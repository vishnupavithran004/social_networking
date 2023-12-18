from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
from users.models import User


class FriendRequest(models.Model):
    RECEIVED = 'received'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    FRIENDSHIP_STATUS = (
        (RECEIVED, "Friend Request Received"),
        (ACCEPTED, "Friend Request Accepted"),
        (REJECTED, "Friend Request Rejected"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user')
    friend = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='requested_by')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=FRIENDSHIP_STATUS,
                              default=RECEIVED, max_length=15)

    class Meta:
        unique_together = ('user', 'friend')

    def validate_user(self):
        if self.user == self.friend:
            raise ValidationError('A user cannot be friends with themselves.')

    def save(self, *args, **kwargs):
        self.validate_user()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} - {self.friend.email}"
