from rest_framework import serializers

from photo_manager.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ("title", "albumId", "image_url")


class PhotoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ("id", "title", "albumId", "width", "height", "dominant_color", "image_file")
