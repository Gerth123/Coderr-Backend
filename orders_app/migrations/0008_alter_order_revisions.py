# Generated by Django 5.1.3 on 2025-01-07 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders_app', '0007_alter_order_offer_detail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='revisions',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]