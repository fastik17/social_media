from django.contrib import admin

from posts import models


@admin.register(models.Post)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'title')
    readonly_fields = ('created_at', 'last_updated_at')


@admin.register(models.Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'object_id')
    readonly_fields = ('created_at',)
