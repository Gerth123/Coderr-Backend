# Generated by Django 5.1.3 on 2024-12-31 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users_auth_app', '0005_alter_userprofile_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='slug',
        ),
    ]
