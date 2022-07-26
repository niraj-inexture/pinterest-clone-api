from django.db import models

# Create your models here.

class Topic(models.Model):
    topic_name = models.CharField(max_length=100)
    total_likes = models.IntegerField(default=0)

    def __str__(self):
        return str(self.topic_name)
