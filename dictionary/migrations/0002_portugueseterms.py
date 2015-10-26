# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PortugueseTerms',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('display_order', models.PositiveSmallIntegerField(default=0)),
                ('word_entry', models.ForeignKey(to='dictionary.WordEntry')),
            ],
        ),
    ]
