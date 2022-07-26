from django.urls import path
from . import views

urlpatterns = [
    path('create-topic/', views.TopicClassView.as_view(), name='create-topic'),
    path('trending-topics/', views.TrendingTopicClassView.as_view(), name='trending-topics'),
    path('trending-topic-images/',views.TrendingTopicImageClassView.as_view(),name='trending-topic-images'),
    path('delete-topic/<int:topic_id>', views.TopicClassView.as_view(), name='delete-topic')
 ]