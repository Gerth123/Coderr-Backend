# Generated by Django 5.1.3 on 2024-12-30 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_auth_app', '0004_alter_userprofile_options_userprofile_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='type',
            field=models.CharField(choices=[('business', 'Business'), ('personal', 'Personal')], max_length=10),
        ),
    ]
