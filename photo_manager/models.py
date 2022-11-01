from tempfile import NamedTemporaryFile
from urllib.request import urlopen, Request

import scipy as scipy
from django.core.files import File
from django.db import models
from django.utils.text import slugify


class Photo(models.Model):
    title = models.CharField(max_length=255)
    albumId = models.IntegerField()
    image_file = models.ImageField(
        upload_to="photos", width_field="image_width", height_field="image_height"
    )
    image_width = models.IntegerField()
    image_height = models.IntegerField()
    image_url = models.URLField()

    @property
    def dominant_color(self):
        im = self.image_file.open()
        im = im.resize((150, 150))  # optional, to reduce time
        ar = scipy.misc.fromimage(im)
        shape = ar.shape
        ar = ar.reshape(scipy.product(shape[:2]), shape[2])

        codes, dist = scipy.cluster.vq.kmeans(ar, 5)

        vecs, dist = scipy.cluster.vq.vq(ar, codes)  # assign codes
        counts, bins = scipy.histogram(vecs, len(codes))  # count occurrences

        index_max = scipy.argmax(counts)  # find most frequent
        peak = codes[index_max]
        colour = ''.join(chr(c) for c in peak).encode('hex')
        return colour

    def save(self, *args, **kwargs):
        if self.image_url and not self.image_file:
            img_temp = NamedTemporaryFile(delete=True)
            req = Request(
                url=self.image_url,
                headers={'User-Agent': 'XYZ/3.0'}
            )
            img_temp.write(urlopen(req, timeout=10).read())
            img_temp.flush()
            self.image_file.save(f"{slugify(self.title)}.png", File(img_temp))
        return super(Photo, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.title)
