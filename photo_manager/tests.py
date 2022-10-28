from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from photo_manager.models import Photo

LIST_URL = reverse("photo-manager:photo-list")


def sample_photo():
    defaults = {
        "title": "test photo",
        "albumId": 2,
        "image_url": "https://via.placeholder.com/150/92c952"
    }
    return Photo.objects.create(**defaults)


class PhotoManagerTests(TestCase):
    def test_create_photo(self):
        payload = {
            "title": "green photo",
            "albumId": 1,
            "image_url": "https://via.placeholder.com/600/92c952"
        }
        res = self.client.post(LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn("title", res.data)
        self.assertIn("albumId", res.data)
        self.assertIn("width", res.data)
        self.assertIn("height", res.data)
        self.assertIn("dominant_color", res.data)
        self.assertIn("image_file", res.data)

    def test_list_photo(self):
        sample_photo()
        sample_photo()

        res = self.client.get(LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], 2)
