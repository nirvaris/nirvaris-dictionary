# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='word_entry_comments', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=70)),
                ('location', models.CharField(max_length=70)),
                ('is_tribal', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=155)),
                ('file_name', models.CharField(max_length=255)),
                ('display_order', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('display', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='WordClass',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('display_order', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='WordContent',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='word_entries_content')),
            ],
        ),
        migrations.CreateModel(
            name='WordEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('relative_url', models.CharField(unique=True, max_length=155)),
                ('word', models.CharField(max_length=100)),
                ('short_description', models.CharField(max_length=155)),
                ('audio_file', models.CharField(blank=True, null=True, max_length=255)),
                ('phonetics', models.CharField(blank=True, null=True, max_length=255)),
                ('template', models.CharField(max_length=50, default='word-entry-default.html')),
                ('is_published', models.BooleanField(default=False)),
                ('access_count', models.BigIntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='word_entries')),
                ('languages', models.ManyToManyField(to='dictionary.Language', related_name='word_entries')),
                ('tags', models.ManyToManyField(to='dictionary.Tag', related_name='tags')),
                ('word_classes', models.ManyToManyField(to='dictionary.WordClass', related_name='word_entries')),
                ('word_content', models.ForeignKey(to='dictionary.WordContent', related_name='word_entries', null=True)),
                ('words_related', models.ManyToManyField(to='dictionary.WordEntry', related_name='word_related_to')),
            ],
        ),
        migrations.AddField(
            model_name='picture',
            name='word_content',
            field=models.ForeignKey(to='dictionary.WordContent', related_name='pictures'),
        ),
        migrations.AddField(
            model_name='comment',
            name='word_entry',
            field=models.ForeignKey(to='dictionary.WordEntry', related_name='word_entry_comments'),
        ),
    ]
