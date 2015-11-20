# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0003_auto_20151117_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordentry',
            name='word',
            field=models.CharField(max_length=100),
        ),
    ]
