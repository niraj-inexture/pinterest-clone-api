from django.contrib.auth.hashers import check_password
from rest_framework import serializers

from user.models import RegisterUser, FollowPeople, Boards


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'country', 'gender',
                  'profile_image']
        extra_kwargs = {
            'email': {'required': True}
        }

    def validate_first_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError('Firstname only contain alphabet')
        return value

    def validate_last_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError('Lastname only contain alphabet')
        return value

    def validate_email(self, value):
        result = RegisterUser.objects.filter(email=value).exists()
        if result:
            raise serializers.ValidationError('Email id already exists')
        return value


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterUser
        fields = ['email', 'password']
        extra_kwargs = {
            'email': {'required': True}
        }


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterUser
        fields = ['username', 'first_name', 'last_name', 'email', 'country', 'gender', 'profile_image']

    def validate_email(self, value):
        user = self.context['user']
        result = RegisterUser.objects.exclude(pk=user.pk).filter(email=value).exists()
        if result:
            raise serializers.ValidationError('Email id already exists')
        return value

    def validate_first_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError('Firstname only contain alphabet')
        return value

    def validate_last_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError('Lastname only contain alphabet')
        return value


class FollowUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowPeople
        exclude = ['following']

    def validate(self, attrs):
        following_id = self.context.get('user').id
        follower_id = attrs.get('follower').id
        if following_id == follower_id:
            raise serializers.ValidationError("You can not follow yourself")
        return attrs


class EmailFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterUser
        fields = ['email']
        extra_kwargs = {
            'email': {'required': True}
        }


class UpdatePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = RegisterUser
        fields = ['password', 'new_password']

    def validate(self, attrs):
        password = attrs.get('password')
        new_password = attrs.get('new_password')
        user = self.context.get('user')

        if not check_password(password, user.password):
            raise serializers.ValidationError('Old password does not match')

        user.set_password(new_password)
        user.save()
        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, required=True)
    confirm_password = serializers.CharField(max_length=255, required=True)

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        user = self.context.get('user')

        if password != confirm_password:
            raise serializers.ValidationError('Password does not match!')

        user.set_password(password)
        user.save()
        return attrs


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boards
        exclude = ['user']
