# Generated by Django 5.1.3 on 2025-01-06 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_auth_app', '0008_userprofile_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='profile_picture',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='file',
            field=models.ImageField(blank=True, null=True, upload_to='files/'),
        ),
    ]
