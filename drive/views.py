from django.views.generic import ListView
from .models import Resource
from utils.files import convert_size, parse_data
from asgiref.sync import async_to_sync


class ListResources(ListView):
    model = Resource
    template_name = 'index.html'
    context_object_name = 'resources'

    def get_queryset(self):
        public_key: str = self.request.GET['public_key']
        async_to_sync(parse_data)(public_key, "")

        return super().get_queryset()
