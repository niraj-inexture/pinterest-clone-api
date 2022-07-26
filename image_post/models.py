from cloudinary.models import CloudinaryField
from django.db import models

# Create your models here.
from django.utils import timezone

from topic.models import Topic
from user.models import RegisterUser

IMAGE_TYPE = (
    ('Public', 'Public'),
    ('Private', 'Private'),
)


class ImageStore(models.Model):
    user = models.ForeignKey(RegisterUser, on_delete=models.CASCADE)
    topic = models.ManyToManyField(Topic)
    description = models.TextField()
    image_path = CloudinaryField('image')
    approve_status = models.BooleanField(default=False)
    image_type = models.CharField(choices=IMAGE_TYPE, max_length=15)
    image_upload_date = models.DateField(default=timezone.now)


class ImageLike(models.Model):
    user = models.ForeignKey(RegisterUser, on_delete=models.CASCADE, related_name='user_like')
    like_user = models.ForeignKey(RegisterUser, on_delete=models.CASCADE, related_name='follower_like')
    image_path = models.ForeignKey(ImageStore, on_delete=models.CASCADE)


class ImageSave(models.Model):
    user = models.ForeignKey(RegisterUser, on_delete=models.CASCADE)
    image_path = models.ForeignKey(ImageStore, on_delete=models.CASCADE)


class BoardImages(models.Model):
    user = models.ForeignKey(RegisterUser, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    image_post = models.ForeignKey(ImageStore, on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.ForeignKey(RegisterUser, on_delete=models.CASCADE)
    image_path = models.ForeignKey(ImageStore, on_delete=models.CASCADE)
    comment = models.TextField()
