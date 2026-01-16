"""file with celery tasks for 'users' Django's app."""

from io import BytesIO

from celery import Task, shared_task
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from PIL import Image

from .models import Profile


@shared_task(bind=True)
def process_avatar(self: Task, profile_id: int) -> bool:
    """Create different sized thumbnail images for avatar.

    Args:
        self (Task): Task object is returned by Celery.
        profile_id (int): ID of the Profile avatar is processed.

    Returns:
        bool: True if avatar is processed successfully. 

    """
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

                    # returns f'users/{self.user.pk}/avatars/{size}.webp'
                    path = profile.user_avatar_path(f'{size}.webp')
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
        if default_storage.exists(avatar_to_del):
            default_storage.delete(avatar_to_del)

        return True

    except Exception as e:
        print(e)

    return False
