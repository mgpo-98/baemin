from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from imagekit.models import ProcessedImageField

from imagekit.processors import Thumbnail

from imagekit.processors import ResizeToFill


class User(AbstractUser):

    followings = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers"
    )


class Profile(models.Model):
    image = models.ImageField(upload_to="", default="캡처.jpg")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
