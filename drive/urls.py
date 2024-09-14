from django.contrib import admin
from django.urls import path
from .views import ListResources

urlpatterns = [
    path('', ListResources.as_view(), name='resources'),
]
