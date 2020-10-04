from rest_framework import serializers
from posts.models import Post
from posts.utils import liked


class PostSerializers(serializers.ModelSerializer):
    liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'liked', 'total_likes')
        read_only_fields = ('id', 'user', 'created_at', 'last_updated_at')

    def get_liked(self, obj) -> bool:
        """Check if a user has liked this tweet (`obj`)."""
        user = self.context.get('request').user
        return liked(obj, user)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        post = super().create(validated_data)

        return post
