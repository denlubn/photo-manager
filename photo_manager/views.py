from django.shortcuts import render
from rest_framework import viewsets

from photo_manager.models import Photo
from photo_manager.serializers import PhotoListSerializer, PhotoSerializer


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return PhotoListSerializer

        return PhotoSerializer
