from django.contrib import admin
from .models import Notification

# Register your models here.

from .models import *

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(Followers)
admin.site.register(Comment)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'notification_type', 'post', 'created_at', 'is_read')
    list_filter = ('notification_type', 'created_at', 'is_read')
    search_fields = ('sender__username', 'receiver__username')
