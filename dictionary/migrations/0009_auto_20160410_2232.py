# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-10 22:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0008_auto_20160410_2229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wordcontent',
            name='references',
        ),
        migrations.AddField(
            model_name='wordcontent',
            name='references',
            field=models.ManyToManyField(null=True, related_name='words_referenced', to='dictionary.WordContentReference'),
        ),
    ]
