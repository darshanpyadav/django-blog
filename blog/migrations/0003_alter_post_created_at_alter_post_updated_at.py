# Generated by Django 4.0.4 on 2022-05-12 15:35

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_post_created_at_alter_post_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 12, 15, 35, 56, 955994, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 12, 15, 35, 56, 956358, tzinfo=utc)),
        ),
    ]