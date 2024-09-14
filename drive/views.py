import asyncio
import math
import aiohttp
import environ
import requests
from asgiref.sync import sync_to_async, async_to_sync
from django.views.generic import ListView

from .models import Resource

env = environ.Env()
environ.Env.read_env()
BASE_URL = 'https://cloud-api.yandex.net/v1/disk/public/resources'


@sync_to_async
def create_resource(data) -> Any:
    if Resource.objects.filter(resource_id__exact=data['resource_id']).count() != 0:
        return

    return Resource.objects.create(
        resource_id=data['resource_id'],
        name=data['name'],
        file_url=data['public_key'],
        preview_url=data.get('preview', None),
        type=data['type'],
        mime_type=data.get('mime_type', None),
        size=data,
        created_at=data['created'],
        updated_at=data['modified']
    )


async def parse_data(public_key: str, path: str = None, preview_crop: str = 'true'):
    payload = {
        'public_key': public_key,
        'path': path,
        'preview_crop': preview_crop
    }
    headers = {'Authorization': env('OAUTH2TOKEN')}

    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, params=payload, headers=headers) as response:
            response_data = await response.json()

            for r in response_data['_embedded']['items']:
                await create_resource(r)


def save_data():
    pass


class ListResources(ListView):
    model = Resource
    template_name = 'index.html'
    context_object_name = 'resources'

    def get_queryset(self):
        public_key: str = self.request.GET['public_key']
        async_to_sync(parse_data)(public_key, "")

        return super().get_queryset()
