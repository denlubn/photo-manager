from django.urls import path, include
from rest_framework import routers

from photo_manager.views import PhotoViewSet

router = routers.DefaultRouter()
router.register("photos", PhotoViewSet)

urlpatterns = [
    path("", include(router.urls))
]

app_name = "photo-manager"
