from rest_framework import serializers
from .models import Post

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
        read_only=True
    )
    
    class Meta:
        model = Post
        fields = '__all__'