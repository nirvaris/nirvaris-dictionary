# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-10 22:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0007_auto_20160328_1642'),
    ]

    operations = [
        migrations.CreateModel(
            name='WordContentReference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=1024, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='language',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='language_parent', to='dictionary.Language'),
        ),
        migrations.AddField(
            model_name='wordcontent',
            name='references',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='words_referenced', to='dictionary.WordContentReference'),
        ),
    ]
