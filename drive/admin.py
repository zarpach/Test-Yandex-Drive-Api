from django.contrib import admin
from .models import Resource


@admin.register(Resource)
class ResourcesAdmin(admin.ModelAdmin):
    pass
