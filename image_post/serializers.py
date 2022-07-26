from rest_framework import serializers

from image_post.models import ImageStore, ImageLike, ImageSave, BoardImages, Comment


class ImageStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageStore
        exclude = ['user']

    def validate_image_path(self,value):
        img_type = value.name.split('.')
        type_list = ['BMP', 'JPEG', 'PNG', 'TIFF', 'WEBP', 'JPG']
        if img_type[-1].upper() not in type_list:
            raise serializers.ValidationError('Image can upload in bmp, jpeg, png, tiff or webp format.')
        return value


class ImageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageStore
        fields = ['id', 'description', 'image_path', 'image_upload_date', 'user', 'topic']


class ImageLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageLike
        exclude = ['like_user']


class ImageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageStore
        fields = ['topic', 'description']


class ImageSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageSave
        exclude = ['user']


class ImageHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageStore
        fields = '__all__'


class BoardImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardImages
        exclude = ['user']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['user']
