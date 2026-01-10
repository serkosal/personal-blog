from io import BytesIO

from celery import Task, shared_task
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from PIL import Image

from .models import Profile


@shared_task(bind=True)
def process_avatar(self: Task, profile_id: int) -> bool:
    profile = Profile.objects.filter(pk=profile_id).first()

    if not profile or not profile.avatar:
        return False

    avatar = profile.avatar

    try:
        with avatar.open('rb') as f:
            for size in Profile.AVATAR_SIZES:
                with Image.open(f) as img:
                    img_converted = img.convert('RGBA')
                    img_converted.thumbnail((size, size))

                    path = profile.user_directory_path(f'{size}.webp')
                    buf = BytesIO()
                    img_converted.save(buf, format='WEBP', quality=80, method=6)

                    buf.seek(0)

                    if default_storage.exists(str(path)):
                        default_storage.delete(str(path))

                    default_storage.save(str(path), ContentFile(buf.read()))

        avatar_to_del = avatar.name
        avatar = None
        profile.avatar_is_set = True

        profile.save(update_fields=['avatar', 'avatar_is_set'])
        default_storage.delete(avatar_to_del)

        return True

    except Exception as e:
        print(e)

    return False
