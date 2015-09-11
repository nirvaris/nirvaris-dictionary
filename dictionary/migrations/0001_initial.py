# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('content', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(related_name='word_entry_comments', to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='MetaTag',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('property', models.CharField(max_length=70)),
                ('content', models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('description', models.CharField(max_length=155)),
                ('full_file_name', models.CharField(max_length=255, unique=True)),
                ('small_file_name', models.CharField(max_length=255, unique=True)),
                ('tiny_file_name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=10, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='WordEntry',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=70)),
                ('word', models.CharField(max_length=100, unique=True)),
                ('short_description', models.CharField(max_length=155)),
                ('scientific_name', models.CharField(max_length=255, null=True)),
                ('audio_file', models.CharField(max_length=255, null=True)),
                ('phonetics', models.CharField(max_length=255, null=True)),
                ('meaning', models.TextField()),
                ('curiosities', models.TextField()),
                ('template', models.CharField(max_length=50, default='default-word-entries.html')),
                ('access_count', models.BigIntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(related_name='word_entries', to=settings.AUTH_USER_MODEL)),
                ('languages', models.ManyToManyField(related_name='word_entries', to='dictionary.Language')),
                ('tags', models.ManyToManyField(related_name='tags', to='dictionary.Tag')),
            ],
        ),
        migrations.AddField(
            model_name='picture',
            name='word_entry',
            field=models.ForeignKey(to='dictionary.WordEntry'),
        ),
        migrations.AddField(
            model_name='metatag',
            name='word_entry',
            field=models.ForeignKey(to='dictionary.WordEntry'),
        ),
        migrations.AddField(
            model_name='comment',
            name='word_entry',
            field=models.ForeignKey(related_name='word_entry_comments', to='dictionary.WordEntry'),
        ),
    ]
