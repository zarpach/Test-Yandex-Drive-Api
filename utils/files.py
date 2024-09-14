import aiohttp
import environ
from asgiref.sync import sync_to_async, async_to_sync
from drive.models import Resource
from django.conf import settings
import asyncio
import math
import os.path

env = environ.Env()
environ.Env.read_env()


def get_file_extension(filename: str) -> str:
    extension = os.path.splitext(filename)[1][1:]
    return extension


def convert_size(size_bytes: int) -> str:
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def validate(key, val) -> any:
    result: any = None
    try:
        result = key[val]
    except Exception as e:
        print(e)

    if val == 'size' and result is not None:
        result = convert_size(result)

    return result


@sync_to_async
def create_resource(data) -> any:
    if Resource.objects.filter(resource_id__exact=data['resource_id']).count() != 0:
        return

    return Resource.objects.create(
        resource_id=validate(data, 'resource_id'),
        name=validate(data, 'name'),
        file_url=validate(data, 'public_key'),
        file_extension=get_file_extension(validate(data, 'name')),
        preview_url=validate(data, 'preview'),
        type=validate(data, 'type'),
        media_type=validate(data, 'media_type'),
        size=validate(data, 'size'),
        created_at=validate(data, 'created'),
        updated_at=validate(data, 'modified')
    )


async def parse_data(public_key: str, path: str = None, preview_crop: str = 'true'):
    payload = {
        'public_key': public_key,
        'path': path,
        'preview_crop': preview_crop
    }
    headers = {'Authorization': env('OAUTH2TOKEN')}

    async with aiohttp.ClientSession() as session:
        async with session.get(settings.EXTERNAL_DRIVE_BASE_URL, params=payload, headers=headers) as response:
            response_data = await response.json()

            for r in response_data['_embedded']['items']:
                await create_resource(r)
