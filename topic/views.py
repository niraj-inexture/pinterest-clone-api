# Create your views here.
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

from image_post.models import ImageStore
from topic.models import Topic
from topic.serializers import TopicSerializer, TrendingTopicImagesSerializer
from rest_framework.response import Response


class TopicClassView(APIView):
    permission_classes = [IsAdminUser]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TopicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'data': [],
                'status': True,
                'message': 'Topic created successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            'data': [serializer.errors],
            'status': False,
            'message': 'Topic not created!'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, topic_id):
        topic_obj = Topic.objects.filter(id=topic_id).first()
        if topic_obj:
            topic_obj.delete()
            response = {
                'data': [],
                'status': True,
                'message': 'Topic deleted successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'data': [],
                'status': False,
                'message': 'Topic not found!'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class TrendingTopicClassView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        trending_topic_data = Topic.objects.all().order_by('-total_likes')[:3]
        if trending_topic_data.exists():
            trending_topic_serializer = TopicSerializer(trending_topic_data, many=True)
            response = {
                'data': [trending_topic_serializer.data],
                'status': True,
                'message': 'Trending topics get successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'data': [],
                'status': False,
                'message': 'No topic available'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class TrendingTopicImageClassView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        topic_id = request.data.get('topic_id')
        topic_obj = Topic.objects.filter(id=topic_id).first()
        if topic_obj:
            trending_topic_image = ImageStore.objects.filter(topic=topic_id)
            trending_topic_image_serializer = TrendingTopicImagesSerializer(trending_topic_image, many=True)
            response = {
                'data': [trending_topic_image_serializer.data],
                'status': True,
                'message': 'Trending topic images get successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'data': [],
                'status': False,
                'message': 'Topic not available'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
