# Generated by Django 5.1.5 on 2025-01-31 05:15

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("authuser", "0013_alter_comment_user_profile"),
    ]

    operations = [
        migrations.RenameField(
            model_name="comment",
            old_name="user_profile",
            new_name="profile",
        ),
    ]
