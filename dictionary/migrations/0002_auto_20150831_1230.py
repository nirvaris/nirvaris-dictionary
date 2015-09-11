# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordentry',
            name='relative_url',
            field=models.CharField(default='/', max_length=155, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='wordentry',
            name='word',
            field=models.CharField(max_length=100),
        ),
    ]
