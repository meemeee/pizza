# Generated by Django 2.1.5 on 2019-11-06 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('orders', '0028_auto_20191106_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='content_type',
            field=models.ForeignKey(limit_choices_to=models.Q(models.Q(('app_label', 'sub'), ('model', 'OrderSubs')), models.Q(('app_label', 'pasta'), ('model', 'OrderPasta')), models.Q(('app_label', 'dp'), ('model', 'OrderDP')), _connector='OR'), null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='item',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='tag',
            field=models.SlugField(null=True),
        ),
    ]