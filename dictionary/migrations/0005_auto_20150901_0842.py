# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0004_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordentry',
            name='template',
            field=models.CharField(max_length=50, default='word-entry-default.html'),
        ),
    ]
