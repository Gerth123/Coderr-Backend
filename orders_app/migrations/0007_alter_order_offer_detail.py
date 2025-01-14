# Generated by Django 5.1.3 on 2025-01-07 18:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers_app', '0009_alter_offerdetail_revisions'),
        ('orders_app', '0006_rename_offer_detail_id_order_offer_detail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='offer_detail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='offers_app.offerdetail'),
        ),
    ]
