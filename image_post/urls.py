from django.urls import path
from . import views

urlpatterns = [
    path('image-upload/', views.ImageUploadClassView.as_view(),name='image-upload'),
    path('image-detail/<int:id>',views.ImageDetailClassView.as_view(),name='image-detail'),
    path('image-like/',views.ImageLikeClassView.as_view(),name='image-like'),
    path('image-unlike/',views.ImageLikeClassView.as_view(),name='image-unlike'),
    path('image-save/',views.ImageSaveClassView.as_view(),name='image-save'),
    path('image-unsave/',views.ImageSaveClassView.as_view(),name='image-unsave'),
    path('image-update/<int:id>',views.ImageUpdateClassView.as_view(),name='image-update'),
    path('image-history/',views.ImageHistoryClassView.as_view(),name='image-history'),
    path('image-delete/',views.ImageUploadClassView.as_view(),name='image-delete'),
    path('board-images/<int:id>',views.BoardImagesClassView.as_view(), name='board-images'),
    path('board-save-image/',views.BoardImagesClassView.as_view(), name='board-save-image'),
    path('delete-board-image/<int:id>/<int:topic_id>', views.BoardImagesClassView.as_view(), name='delete-board-image'),
    path('create-comment/', views.CommentClassView.as_view(), name='create-comment'),
    path('delete-comment/<int:comment_id>', views.CommentClassView.as_view(), name='delete-comment'),
    path('update-comment/<int:comment_id>',views.CommentClassView.as_view(), name='update-comment'),
]