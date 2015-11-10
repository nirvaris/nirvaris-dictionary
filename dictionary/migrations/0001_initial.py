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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('content', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('author', models.ForeignKey(related_name='word_entry_comments', null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=70)),
                ('location', models.CharField(max_length=70)),
                ('is_tribal', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('description', models.CharField(max_length=155)),
                ('file_name', models.CharField(unique=True, max_length=255)),
                ('display_order', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('display', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='WordContent',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('short_description', models.CharField(max_length=155)),
                ('content', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='word_entries_content')),
            ],
        ),
        migrations.CreateModel(
            name='WordEntry',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('relative_url', models.CharField(unique=True, max_length=155)),
                ('word', models.CharField(max_length=100)),
                ('audio_file', models.CharField(blank=True, null=True, max_length=255)),
                ('phonetics', models.CharField(blank=True, null=True, max_length=255)),
                ('template', models.CharField(default='word-entry-default.html', max_length=50)),
                ('is_published', models.BooleanField(default=False)),
                ('access_count', models.BigIntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='word_entries')),
                ('languages', models.ManyToManyField(related_name='word_entries', to='dictionary.Language')),
                ('tags', models.ManyToManyField(related_name='tags', to='dictionary.Tag')),
                ('word_content', models.ForeignKey(to='dictionary.WordContent', related_name='word_entries')),
            ],
        ),
        migrations.CreateModel(
            name='WordFunction',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('display_order', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='WordRelated',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('word_entry', models.ForeignKey(to='dictionary.WordEntry', related_name='word_has_related')),
                ('word_related', models.ForeignKey(to='dictionary.WordEntry', related_name='words_related')),
            ],
        ),
        migrations.CreateModel(
            name='WordType',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('display_order', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='wordentry',
            name='word_functions',
            field=models.ManyToManyField(related_name='word_entries', to='dictionary.WordFunction'),
        ),
        migrations.AddField(
            model_name='wordentry',
            name='word_types',
            field=models.ManyToManyField(related_name='word_entries', to='dictionary.WordType'),
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
