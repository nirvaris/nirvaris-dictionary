# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-28 14:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0002_auto_20160111_1038'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='author_ip',
            field=models.GenericIPAddressField(default=0),
            preserve_default=False,
        ),
    ]