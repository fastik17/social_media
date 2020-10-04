from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class Like(models.Model):
    _limit_generic = models.Q(app_label='posts', model__iexact='post') | \
                     models.Q(app_label='posts', model__iexact='comment')
    user = models.ForeignKey('authentication.User', models.CASCADE, related_name='likes')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, editable=False)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = 'likes'
        ordering = ('-id',)

    def __str__(self):
        return f"{self.user}, {self.content_object}"


class Post(models.Model):
    user = models.ForeignKey('authentication.User', models.CASCADE, related_name="posts")
    title = models.CharField(max_length=255)
    body = models.TextField(null=True, blank=True)
    likes = GenericRelation(Like, related_query_name='posts')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_table = 'posts'
        ordering = ('-id',)

    def __str__(self):
        return f"{self.id}, {self.title}"

    def total_likes(self):
        return self.likes.count()
