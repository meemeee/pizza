# Generated by Django 2.1.5 on 2019-11-04 07:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0020_auto_20191104_0556'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderSubsX',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('name', models.ForeignKey(limit_choices_to={'steak_subs_extra': True, 'subs_extra': True}, on_delete=django.db.models.deletion.CASCADE, to='orders.SubsType')),
            ],
        ),
    ]
