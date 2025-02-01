# Generated by Django 5.1.5 on 2025-01-30 08:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authuser", "0005_alter_followers_follower_alter_followers_user_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="followers",
            name="follower",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="follower",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="followers",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="following",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="likepost",
            name="post_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="authuser.post"
            ),
        ),
        migrations.AlterField(
            model_name="likepost",
            name="username",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
