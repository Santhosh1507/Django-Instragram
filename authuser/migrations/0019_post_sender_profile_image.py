# Generated by Django 5.1.5 on 2025-03-17 08:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authuser", "0018_notification_sender_profile_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="sender_profile_image",
            field=models.URLField(blank=True, null=True),
        ),
    ]
