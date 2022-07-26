# Create your models here.
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.db import models

from topic.models import Topic

COUNTRY_CHOICES = (
    ("India", "India"),
    ("Afghanistan", "Afghanistan"),
    ("Brazil", "Brazil"),
    ("Australia", "Australia"),
    ("Canada", "Canada"),
    ("France", "France"),
    ("Colombia", "Colombia"),
    ("Germany", "Germany"),
    ("Indonesia", "Indonesia"),
    ("Italy", "Italy"),
    ("Japan", "Japan")
)

GENDER_CHOICES = [
    ("Male", 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other')
]


class User(AbstractUser):
    class Meta(AbstractUser.Meta):
        abstract = True


class RegisterUser(User):
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10)
    profile_image = models.ImageField(upload_to='profile_image', default='default.jpg')
    country = models.CharField(choices=COUNTRY_CHOICES, max_length=30)

    class Meta:
        abstract = False


class FollowPeople(models.Model):
    follower = models.ForeignKey(RegisterUser, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(RegisterUser, on_delete=models.CASCADE, related_name='following')


class Boards(models.Model):
    user = models.ForeignKey(RegisterUser, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
