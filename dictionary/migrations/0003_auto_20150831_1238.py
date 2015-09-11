# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0002_auto_20150831_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordentry',
            name='audio_file',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='wordentry',
            name='curiosities',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='wordentry',
            name='phonetics',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='wordentry',
            name='scientific_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
