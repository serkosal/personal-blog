from pydantic import ValidationError

from rest_framework import serializers
from ..models import Post
from .post_content import PostContentSchema


class PostSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='blog:api-detail',
        lookup_field='id',
        lookup_url_kwarg='post_id',
    )

    author = serializers.HyperlinkedRelatedField(
        view_name='users:api-detail',
        lookup_field='id',
        lookup_url_kwarg='profile_id',
        read_only=True,
    )

    content = serializers.JSONField()

    def validate_content(self, value):
        try:
            validated = PostContentSchema.model_validate(value, mode='python')
        except ValidationError as err:
            raise serializers.ValidationError(err.errors())

        return validated.model_dump()

    class Meta:
        model = Post
        fields = ['author', 'title', 'url', 'content']
