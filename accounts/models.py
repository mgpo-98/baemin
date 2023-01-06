from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from imagekit.models import ProcessedImageField

from imagekit.processors import Thumbnail

from imagekit.processors import ResizeToFill


class User(AbstractUser):
    image_thumbnail = ProcessedImageField(
        upload_to="accounts/images/",
        blank=True,
        processors=[ResizeToFill(160, 90)],
        format="JPEG",
        options={"quality": 95},
    )
    followings = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers"
    )
    pass


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )ss
    image = models.ImageField(
        upload_to="accounts/images/",
        blank=True,
    )
    thumbnail = ProcessedImageField(
        upload_to="accounts/images/",
        blank=True,
        processors=[Thumbnail(300, 400)],
        format="JPEG",
    )
    status = models.CharField(max_length=100, blank=True)
