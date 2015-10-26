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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('content', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, related_name='word_entry_comments')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='MetaTag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=70)),
                ('property', models.CharField(max_length=70)),
                ('content', models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('description', models.CharField(max_length=155)),
                ('file_name', models.CharField(max_length=255, unique=True)),
                ('display_order', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=10, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='WordEntry',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('relative_url', models.CharField(max_length=155, unique=True)),
                ('title', models.CharField(max_length=70)),
                ('word', models.CharField(max_length=100)),
                ('short_description', models.CharField(max_length=155)),
                ('scientific_name', models.CharField(null=True, max_length=255, blank=True)),
                ('audio_file', models.CharField(null=True, max_length=255, blank=True)),
                ('phonetics', models.CharField(null=True, max_length=255, blank=True)),
                ('meaning', models.TextField()),
                ('curiosities', models.TextField(blank=True)),
                ('template', models.CharField(default='word-entry-default.html', max_length=50)),
                ('is_published', models.BooleanField(default=False)),
                ('access_count', models.BigIntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='word_entries')),
                ('languages', models.ManyToManyField(to='dictionary.Language', related_name='word_entries')),
                ('tags', models.ManyToManyField(to='dictionary.Tag', related_name='tags')),
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
            field=models.ForeignKey(to='dictionary.WordEntry', related_name='word_entry_comments'),
        ),
    ]
