# Generated by Django 2.2.6 on 2019-10-30 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20191030_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toppings',
            name='subs_extra',
            field=models.BooleanField(default=True),
        ),
    ]