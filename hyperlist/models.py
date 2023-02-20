from django.db import models

# Create your models here.
class hyperlink(models.Model):
    url = models.CharField(max_length = 200)
    origin = models.CharField(max_length = 200)

    def __init__(self, url, origin):
        self.url = url
        self.origin = origin