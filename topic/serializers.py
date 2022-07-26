from rest_framework import serializers

from image_post.models import ImageStore
from topic.models import Topic


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = "__all__"

    # def validate_topic_name(self, value):
    #     value='car'
    #     check_topic = Topic.objects.get(topic_name=value)
    #     if check_topic:
    #         raise serializers.ValidationError('Topic already exists')
    #     return value


class TrendingTopicImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageStore
        fields = "__all__"
