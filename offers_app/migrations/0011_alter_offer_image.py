# Generated by Django 5.1.3 on 2025-01-19 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers_app', '0010_alter_offer_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='image',
            field=models.ImageField(blank=True, default='', upload_to='offers/images/'),
        ),
    ]
