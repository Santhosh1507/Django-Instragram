from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

# Profile Model
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField(primary_key=True, default=0)
    bio = models.TextField(blank=True, default='')
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png', null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return self.user.username

# Post Model
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

# LikePost Model
class LikePost(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)  # Boolean field to track if liked

    def __str__(self):
        return f"LikePost by {self.username.username} on {self.post_id.caption}, Liked: {self.liked}"

# Followers Model
class Followers(models.Model):
    user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.follower.username} follows {self.user.username}"

# Comment Model
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return f"Comment by {self.user.username} on post {self.post.id}"

# Notification Model
class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_notifications")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_notifications")
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username} {self.notification_type} {self.receiver.username}"
