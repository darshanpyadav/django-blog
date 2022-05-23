# Generated by Django 4.0.4 on 2022-05-20 12:10

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=True, populate_from='title', unique=True),
        ),
    ]