from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from image_post.models import ImageStore, BoardImages, ImageLike
from image_post.serializers import ImageStoreSerializer, ImageDetailSerializer
from topic.models import Topic
from user.authentication import EmailAuthBackend
from user.models import FollowPeople, RegisterUser, Boards
from user.serializers import UserSerializer, UserLoginSerializer, ProfileUpdateSerializer, FollowUserSerializer, \
    UpdatePasswordSerializer, ResetPasswordSerializer, BoardSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from user.token import account_activation_token, get_tokens_for_user
from user.utils import email_send_to_user, validate_email


# Create your views here.
@method_decorator(csrf_exempt, name="dispatch")
class UserRegisterClassView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data.get('password'))
            user.save()
            response = {
                'data': [],
                'status': True,
                'message': 'User register successfully'
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            'data': [serializer.errors],
            'status': False,
            'message': 'User not register successfully'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserLoginClassView(APIView):

    def post(self, request):
        login_serializer = UserLoginSerializer(data=request.data)
        if login_serializer.is_valid():
            email = login_serializer.data.get('email')
            password = login_serializer.data.get('password')
            email_auth = EmailAuthBackend()
            user = email_auth.authenticate(request, username=email, password=password)
            if user is not None:
                if user.is_active:
                    token = get_tokens_for_user(user)
                    response = {
                        'data': [token],
                        'status': True,
                        'message': 'Login successfully'
                    }
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    response = {
                        'data': [],
                        'status': False,
                        'message': 'Your account is not active!Please first activate your account.'
                    }
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                response = {
                    'data': [],
                    'status': False,
                    'message': 'Login unsuccessfully'
                }
                return Response(response,status=status.HTTP_400_BAD_REQUEST)
        response = {
            'data': [login_serializer.errors],
            'status': False,
            'message': 'User not register successfully'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class TopicListClassView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        topics = Topic.objects.all().values_list('topic_name', flat=True)
        topic_list = list(topics)
        response = {
            'data': [topic_list],
            'status': True,
            'message': 'Topic list get successfully'
        }
        return Response(response, status=status.HTTP_200_OK)


class SearchClassView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search = request.GET.get('search')
        if search != " ":
            search = search.strip()
            images = ImageStore.objects.filter(topic__topic_name__icontains=search, image_type='Public',
                                               approve_status=True)
            image_detail_serializer = ImageDetailSerializer(images, many=True)
            response = {
                'data': [image_detail_serializer.data],
                'status': True,
                'message': 'Images get by search topic successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'data': [],
                'status': False,
                'message': 'Search box value can not empty!'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class HomeClassView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        imagestore_all_image = ImageStore.objects.filter(approve_status=True, image_type='Public')
        if imagestore_all_image.exists():
            img_serializer = ImageStoreSerializer(imagestore_all_image, many=True)
            response = {
                'data': [img_serializer.data],
                'status': True,
                'message': 'All images get successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'data': [],
                'status': True,
                'message': "No data available!"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class ProfileUpdateClassView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        update_profile_serializer = ProfileUpdateSerializer(request.user)
        response = {
            'data': [update_profile_serializer.data],
            'status': True,
            'message': 'Profile data get successfully'
        }
        return Response(response, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user
        update_profile_serializer = ProfileUpdateSerializer(user, data=request.data, context={'user': user},
                                                            partial=True)
        if update_profile_serializer.is_valid():
            update_profile_serializer.save()
            response = {
                'data': [update_profile_serializer.data],
                'status': True,
                'message': 'Profile Updated successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            'data': [update_profile_serializer.errors],
            'status': False,
            'message': 'Profile data not proper validate!'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class FollowClassView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        follow_user_serializer = FollowUserSerializer(data=request.data, context={'user': request.user})
        if follow_user_serializer.is_valid():
            follow_user_serializer.save(following=request.user)
            response = {
                'data': [follow_user_serializer.data],
                'status': True,
                'message': 'Follow User successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            'data': [follow_user_serializer.errors],
            'status': False,
            'message': 'Follow data not validate properly!'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        following_id = request.data.get('following')
        user_validate = RegisterUser.objects.filter(id=following_id).first()
        if user_validate:
            unfollow_user = FollowPeople.objects.filter(follower=request.user.id, following=following_id).first()
            if unfollow_user:
                unfollow_user.delete()
                response = {
                    'data': [],
                    'status': True,
                    'message': 'Unfollow user successfully'
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    'data': [],
                    'status': False,
                    'message': 'You can not follow this user'
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {
                'data': [],
                'status': False,
                'message': 'User not available'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserAccountClassView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = RegisterUser.objects.get(id=request.user.id)
        user.delete()
        response = {
            'data': [],
            'status': True,
            'message': 'User deleted successfully'
        }
        return Response(response, status=status.HTTP_200_OK)


class DeactivateUserAccountClassView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = RegisterUser.objects.get(id=request.user.id)
        user.is_active = False
        user.save()
        response = {
            'data': [],
            'status': True,
            'message': 'User account deactivate successfully'
        }
        return Response(response, status=status.HTTP_200_OK)


class EmailForActivateClassView(APIView):

    def post(self, request):
        user = validate_email(request)
        if not user.is_active:
            data = {
                'email': user.email,
                'mail_subject': 'Activation link has been sent to your email id',
                'user': user,
                'request': request,
                'msg': 'Please click on the link to activate your account : '
            }
            email_send_to_user(data)
            response = {
                'data': [],
                'status': True,
                'message': 'email successfully send to your email id.'
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'data': [],
                'status': False,
                'message': 'You are already activate!'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ActivateAccountClassView(APIView):

    def put(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = RegisterUser.objects.get(pk=uid)
        except RegisterUser.DoesNotExist:
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            response = {
                'data': [],
                'status': True,
                'message': 'Thank you for your email confirmation. Now you can login your account.'
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'data': [],
                'status': False,
                'message': 'Activation link is invalid!'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UpdatePasswordClassView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        update_password_serializer = UpdatePasswordSerializer(data=request.data, context={'user': request.user})
        if update_password_serializer.is_valid():
            response = {
                'data': [update_password_serializer.data],
                'status': True,
                'message': 'Password update successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            'data': [update_password_serializer.errors],
            'status': False,
            'message': 'Update password data not validate properly!'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetClassView(APIView):

    def put(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = RegisterUser.objects.get(pk=uid)
        except RegisterUser.DoesNotExist:
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            update_password_serializer = ResetPasswordSerializer(data=request.data, context={'user': user})
            if update_password_serializer.is_valid():
                response = {
                    'data': [],
                    'status': True,
                    'message': 'Password reset successfully'
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    'data': [update_password_serializer.errors],
                    'status': False,
                    'message': 'Reset password data not validate properly!'
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {
                'data': [],
                'status': False,
                'message': 'Activation link is invalid!'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class EmailForPasswordResetClassView(APIView):

    def post(self, request):
        user = validate_email(request)
        if user.is_active:
            data = {
                'email': user.email,
                'mail_subject': 'Password reset link has been sent to your email id',
                'user': user,
                'request': request,
                'msg': 'Please click on the link to reset your password : '
            }
            email_send_to_user(data)
            response = {
                'data': [],
                'status': True,
                'message': 'email successfully send to your email id.'
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'data': [],
                'status': False,
                'message': 'First activate your account!'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CreateBoardClassView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        boards_obj = Boards.objects.filter(user=request.user.id)
        board_serializer = BoardSerializer(boards_obj, many=True)
        if boards_obj.exists():
            response = {
                'data': [board_serializer.data],
                'status': True,
                'message': 'All boards get successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'data': [],
                'status': False,
                'message': 'No board available!'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        topic_id = request.data.get('topic')
        validate_board = Boards.objects.filter(user=request.user.id, topic=topic_id).first()
        if not validate_board:
            board_serializer = BoardSerializer(data=request.data)
            if board_serializer.is_valid():
                board_serializer.save(user=request.user)
                response = {
                    'data': [],
                    'status': True,
                    'message': 'Board created successfully'
                }
                return Response(response, status=status.HTTP_201_CREATED)
            response = {
                'data': [board_serializer.errors],
                'status': False,
                'message': 'Board data not proper validate!'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {
                'data': [],
                'status': False,
                'message': 'Board already created!'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        topic_obj = Boards.objects.filter(topic=id, user=request.user.id).first()
        if topic_obj:
            board_obj = Boards.objects.filter(user=request.user.id, topic=id).first()
            if board_obj:
                board_obj.delete()
                BoardImages.objects.filter(user=request.user.id,
                                           topic=id).delete()
                response = {
                    'data': [],
                    'status': True,
                    'message': 'Board deleted successfully'
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    'data': [],
                    'status': False,
                    'message': 'Board not available'
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        else:
            response = {
                'data': [],
                'status': False,
                'message': 'Topic not available!'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
