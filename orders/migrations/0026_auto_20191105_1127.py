# Generated by Django 2.1.5 on 2019-11-05 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0025_auto_20191105_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='order_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.Order'),
        ),
    ]
