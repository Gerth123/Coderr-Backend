# Generated by Django 5.1.3 on 2025-01-06 20:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users_auth_app', '0011_rename_file_userprofile_profile_picture'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='profile_picture',
            new_name='file',
        ),
    ]
