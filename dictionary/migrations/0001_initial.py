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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('content', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('author', models.ForeignKey(null=True, related_name='word_entry_comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=70, unique=True)),
                ('location', models.CharField(max_length=70)),
                ('is_tribal', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('description', models.CharField(max_length=155)),
                ('file_name', models.CharField(max_length=255, unique=True)),
                ('display_order', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('display', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='WordContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('short_description', models.CharField(max_length=155, unique=True)),
                ('content', models.TextField(unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='word_entries_content')),
            ],
        ),
        migrations.CreateModel(
            name='WordEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('relative_url', models.CharField(max_length=155, unique=True)),
                ('word', models.CharField(max_length=100, unique=True)),
                ('audio_file', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('phonetics', models.CharField(blank=True, max_length=255, null=True)),
                ('template', models.CharField(max_length=50, default='word-entry-default.html')),
                ('is_published', models.BooleanField(default=False)),
                ('access_count', models.BigIntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='word_entries')),
                ('languages', models.ManyToManyField(to='dictionary.Language', related_name='word_entries')),
                ('tags', models.ManyToManyField(to='dictionary.Tag', related_name='tags')),
                ('word_content', models.ForeignKey(to='dictionary.WordContent', related_name='word_entries')),
            ],
        ),
        migrations.CreateModel(
            name='WordFunction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('display_order', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='WordRelated',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('word_entry', models.ForeignKey(to='dictionary.WordEntry', related_name='word_has_related')),
                ('word_related', models.ForeignKey(to='dictionary.WordEntry', related_name='words_related')),
            ],
        ),
        migrations.AddField(
            model_name='wordentry',
            name='word_functions',
            field=models.ManyToManyField(to='dictionary.WordFunction', related_name='word_entries'),
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
