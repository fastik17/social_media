from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.serializers import CurrentUserSerializer
from social_media.schema import EmptySchema
from social_media.paginators import ResultPagination

from posts import utils
from posts.serializers import PostSerializers
from posts.models import Post


class PostViewSet(ModelViewSet):
    """
    list:
    Get list of posts

    Get list of user posts

    retrieve:
    Retrieve post

    Retrieve specific post with ID

    create:
    Create new Post

    Create new Post.

    update:
    Update Post with

    Update Post with the given ID.

    partial_update:
    Partial update of Post

    Partial update of Post

    destroy:
    Delete Post

    Delete Post with given ID

    like:
    Like a post instance

    Like a post instance, like return `1`

    dislike:
    Dislike a post instance

    Dislike a post instance, and remove like if it exist

    users:
    Return all users by post id

    Return all users which likes post by id
    """
    serializer_class = PostSerializers
    pagination_class = ResultPagination
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={'204': EmptySchema})
    @action(detail=True, methods=['POST'], permission_classes=(IsAuthenticated,))
    def like(self, request, pk=None):
        obj = self.get_object()
        utils.add_like(obj, request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(responses={'204': EmptySchema})
    @action(detail=True, methods=['POST'], permission_classes=(IsAuthenticated,))
    def dislike(self, request, pk=None):
        obj = self.get_object()
        utils.remove_like(obj, request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(responses={'204': EmptySchema})
    @action(detail=True, methods=['GET'], permission_classes=(IsAuthenticated,))
    def users(self, request, pk=None):
        obj = self.get_object()
        fans = utils.get_fans(obj)
        serializer = CurrentUserSerializer(fans, many=True)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
