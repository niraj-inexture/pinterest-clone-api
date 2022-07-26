# Create your views here.
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from image_post.models import ImageStore, ImageLike, ImageSave, BoardImages, Comment
from image_post.serializers import ImageStoreSerializer, ImageDetailSerializer, ImageLikeSerializer, \
    ImageSaveSerializer, ImageUpdateSerializer, ImageHistorySerializer, BoardImageSerializer, CommentSerializer
from user.models import Boards, FollowPeople
from user.serializers import BoardSerializer, FollowUserSerializer


class ImageUploadClassView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        image_serializer = ImageStoreSerializer(data=request.data)
        if image_serializer.is_valid():
            image_serializer.save(user=request.user)
            response = {
                'data': [],
                'status': True,
                'message': 'Image uploaded successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            'data': [image_serializer.errors],
            'status': False,
            'message': 'Image not uploaded successfully!'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        image_id = request.data.get('image_id')
        image_store_obj = ImageStore.objects.filter(id=image_id, user=request.user.id).first()
        if image_store_obj:
            image_store_obj.delete()
            response = {
                'data': [],
                'status': True,
                'message': 'Image Deleted successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'data': [],
                'status': False,
                'message': 'Image is not upload by current user.'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ImageUpdateClassView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        imagestore_obj = ImageStore.objects.filter(id=id, user=request.user.id).first()
        if imagestore_obj:
            image_update_serializer = ImageUpdateSerializer(imagestore_obj)
            response = {
                'data': [image_update_serializer.data],
                'status': True,
                'message': 'Update image data get successfully!'
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'data': [],
                'status': False,
                'message': 'Image not uploaded by current user'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        image_obj = ImageStore.objects.filter(id=id, user=request.user).first()
        if image_obj:
            imagestore_obj = ImageStore.objects.get(id=id)
            image_update_serializer = ImageUpdateSerializer(imagestore_obj, data=request.data, partial=True)
            if image_update_serializer.is_valid():
                image_update_serializer.save()
                response = {
                    'data': [image_update_serializer.data],
                    'status': True,
                    'message': 'Image updated successfully'
                }
                return Response(response, status=status.HTTP_200_OK)
            response = {
                'data': [image_update_serializer.errors],
                'status': False,
                'message': 'Image not updated successfully!'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {
                'data': [],
                'status': False,
                'message': 'You can not update this image'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ImageHistoryClassView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_uploaded_images = ImageStore.objects.filter(user=request.user.id)
        if user_uploaded_images.exists():
            image_history_serializer = ImageHistorySerializer(user_uploaded_images, many=True)
            response = {
                'data': [image_history_serializer.data],
                'status': True,
                'message': 'Uploaded images get successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'data': [],
                'status': False,
                'message': 'No data available'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ImageDetailClassView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        imagestore_single_image = ImageStore.objects.get(id=id)
        image_serializer = ImageDetailSerializer(imagestore_single_image)

        union_obj = ImageStore.objects.none()
        for i in imagestore_single_image.topic.all():
            filtered_image_store_obj = ImageStore.objects.filter(approve_status=True,
                                                                 image_type='Public').exclude(id=id)
            union_obj = union_obj | filtered_image_store_obj
        related_image_serializer = ImageDetailSerializer(union_obj,many=True)

        save_user_data = ImageSave.objects.filter(user=request.user.id, image_path=id).first()
        image_save_serializer = ImageSaveSerializer(save_user_data)

        follower_data = FollowPeople.objects.filter(follower=imagestore_single_image.user.id).count()

        validate_follow_btn = FollowPeople.objects.filter(following=request.user.id, follower=imagestore_single_image.user.id)
        follow_user_serializer = FollowUserSerializer(validate_follow_btn,many=True)

        validate_like_btn = ImageLike.objects.filter(user=imagestore_single_image.user.id, like_user=request.user.id,
                                                     image_path=imagestore_single_image.id)
        image_like_serializer = ImageLikeSerializer(validate_like_btn, many=True)

        total_likes = ImageLike.objects.filter(image_path=id).count()

        comment_data = Comment.objects.filter(image_path=id)
        comment_serializer = CommentSerializer(comment_data,many=True)

        boards_obj = Boards.objects.filter(user=request.user.id)
        board_serializer = BoardSerializer(boards_obj,many=True)

        response = {
            'data': [image_serializer.data, total_likes, comment_serializer.data, board_serializer.data, related_image_serializer.data,
                     image_save_serializer.data, follower_data, follow_user_serializer.data, image_like_serializer.data],
            'status': True,
            'message': 'Image detail get proper!'
        }
        return Response(response, status=status.HTTP_200_OK)


class ImageLikeClassView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        like_serializer = ImageLikeSerializer(data=request.data)
        if like_serializer.is_valid():
            like_serializer.save(like_user=request.user)
            single_image_data = ImageStore.objects.get(id=request.data['image_path'])
            for topic in single_image_data.topic.all():
                like = topic.total_likes
                like += 1
                topic.total_likes = like
                topic.save()
            response = {
                'data': [],
                'status': True,
                'message': 'Image like successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            'data': [like_serializer.errors],
            'status': False,
            'message': "Image like not validate proper!"
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        img_id = request.data.get('image_id')
        single_image_data = ImageStore.objects.filter(id=img_id).first()
        if single_image_data:
            delete_like = ImageLike.objects.filter(user=request.user.id, image_path=img_id).first()
            if delete_like:
                delete_like.delete()
                for topic in single_image_data.topic.all():
                    like = topic.total_likes
                    like -= 1
                    topic.total_likes = like
                    topic.save()
                response = {
                    'data': [],
                    'status': True,
                    'message': 'Image unlike successfully'
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    'data': [],
                    'status': False,
                    'message': 'Image like not exists'
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {
                'data': [],
                'status': False,
                'message': 'Image does not exists'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ImageSaveClassView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        image_save_serializer = ImageSaveSerializer(data=request.data)
        if image_save_serializer.is_valid():
            image_save_serializer.save(user=request.user)
            response = {
                'data': [],
                'status': True,
                'message': 'Image save successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            'data': [image_save_serializer.errors],
            'status': False,
            'message': "Save image not validate proper!"
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        img_id = request.data.get('image_id')
        single_image_data = ImageStore.objects.filter(id=img_id).first()
        if single_image_data:
            delete_save_image = ImageSave.objects.filter(user=request.user.id, image_path=img_id).first()
            if delete_save_image:
                delete_save_image.delete()
                response = {
                    'data': [],
                    'status': True,
                    'message': 'Image unsaved successfully'
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    'data': [],
                    'status': False,
                    'message': 'Save Image not exists'
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {
                'data': [],
                'status': False,
                'message': 'Image does not exists'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class BoardImagesClassView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        board_image_obj = BoardImages.objects.filter(user=request.user.id, topic=id)
        board_image_serializer = BoardImageSerializer(board_image_obj, many=True)
        if board_image_obj.exists():
            response = {
                'data': [board_image_serializer.data],
                'status': True,
                'message': "Board image get successfully!"
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'data': [],
                'status': False,
                'message': 'No data available'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        board_image_serializer = BoardImageSerializer(data=request.data)
        if board_image_serializer.is_valid():
            topic_id = request.data.get('topic')
            topic_validate = Boards.objects.filter(topic=topic_id).first()
            if topic_validate:
                image_id = request.data.get('image_post')
                board_image_obj = BoardImages.objects.filter(user=request.user.id, topic=topic_id,
                                                             image_post=image_id).first()
                if not board_image_obj:
                    board_image_serializer.save(user=request.user)
                    response = {
                        'data': [],
                        'status': True,
                        'message': 'Image save in board successfully'
                    }
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    response = {
                        'data': [],
                        'status': False,
                        'message': 'Image already save in board!'
                    }
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                response = {
                    'data': [],
                    'status': False,
                    'message': 'Board doest not exists!'
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)

        response = {
            'data': [board_image_serializer.errors],
            'status': False,
            'message': 'Board image not validate proper!'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, topic_id):
        board_image_obj = BoardImages.objects.filter(user=request.user.id, image_post=id, topic=topic_id).first()
        if board_image_obj:
            board_image_obj.delete()
            response = {
                'data': [],
                'status': True,
                'message': 'Image deleted successfully!'
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'data': [],
                'status': False,
                'message': 'Image is not save in board!'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CommentClassView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        comment_serializer = CommentSerializer(data=request.data)
        if comment_serializer.is_valid():
            comment_serializer.save(user=request.user)
            response = {
                'data': [],
                'status': True,
                'message': "Comment successfully!"
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            'data': [comment_serializer.errors],
            'status': False,
            'message': 'comment not validate proper!'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        comment_obj = Comment.objects.filter(user=request.user.id,id=comment_id).first()
        if comment_obj:
            comment_obj.delete()
            response = {
                'data': [],
                'status': True,
                'message': "Comment deleted successfully!"
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'data': [],
                'status': False,
                'message': "Comment id not valid for login user!"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, comment_id):
        comment_obj = Comment.objects.filter(user=request.user.id, id=comment_id).first()
        if comment_obj:
            comment_serializer = CommentSerializer(comment_obj,data=request.data)
            if comment_serializer.is_valid():
                comment_serializer.save()
                response = {
                    'data': [comment_serializer.data],
                    'status': True,
                    'message': "Comment updated successfully!"
                }
                return Response(response, status=status.HTTP_200_OK)
            response = {
                'data': [comment_serializer.errors],
                'status': False,
                'message': "Comment not validate proper!"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {
                'data': [],
                'status': False,
                'message': "Comment id not valid for login user!"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)