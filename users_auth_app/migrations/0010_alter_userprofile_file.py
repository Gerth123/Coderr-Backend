# Generated by Django 5.1.3 on 2025-01-06 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_auth_app', '0009_remove_userprofile_profile_picture_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='file',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/'),
        ),
    ]