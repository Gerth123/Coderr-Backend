# Generated by Django 5.1.3 on 2025-01-22 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_auth_app', '0020_alter_userprofile_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='username',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]