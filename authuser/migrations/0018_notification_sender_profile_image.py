# Generated by Django 5.1.5 on 2025-03-17 07:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authuser", "0017_notification_comment_text"),
    ]

    operations = [
        migrations.AddField(
            model_name="notification",
            name="sender_profile_image",
            field=models.URLField(blank=True, null=True),
        ),
    ]
