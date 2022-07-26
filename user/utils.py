from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.response import Response
from rest_framework import status

from user.models import RegisterUser
from user.serializers import EmailFormSerializer
from user.token import account_activation_token


def email_send_to_user(data):
    current_site = get_current_site(data['request'])
    uid = urlsafe_base64_encode(force_bytes(data['user'].pk))
    token = account_activation_token.make_token(data['user'])
    link = current_site.domain+'/'+uid+'/'+token
    message = data['msg'] + link
    email = EmailMessage(
        subject=data['mail_subject'], body=message, from_email=settings.EMAIL_HOST_USER, to=[data['email']]
    )
    email.send()


def validate_email(request):
    email_form_serializer = EmailFormSerializer(data=request.data)
    if email_form_serializer.is_valid():
        email = request.data.get('email')
        try:
            user = RegisterUser.objects.get(email=email)
        except RegisterUser.DoesNotExist:
            user = None
        if user is not None:
            return user
        else:
            response = {
                'data': [],
                'status': 'error',
                'msg': 'Email id is not valid!'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
