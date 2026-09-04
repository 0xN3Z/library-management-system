from django.conf import settings
from django.db import models


class Profile(models.Model):
    """Extra profile info that doesn't belong on Django's built-in User model."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    age = models.PositiveIntegerField(null=True, blank=True)
    photo = models.ImageField(upload_to="profile_photos/", null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"