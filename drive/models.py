import mimetypes

from django.db import models


class Resource(models.Model):
    resource_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    file_url = models.CharField(max_length=255)
    file_extension = models.CharField(max_length=12, null=True)
    preview_url = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255)
    media_type = models.CharField(max_length=255, null=True)
    size = models.CharField(max_length=25, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
