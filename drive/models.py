import mimetypes

from django.db import models


class Resource(models.Model):
    resource_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    file_url = models.CharField(max_length=255)
    preview_url = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=255, null=True)
    size = models.PositiveIntegerField(null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
