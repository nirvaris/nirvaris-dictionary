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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=70)),
                ('location', models.CharField(max_length=70)),
                ('is_tribal', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('description', models.CharField(max_length=155)),
                ('file_name', models.CharField(unique=True, max_length=255)),
                ('display_order', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=200)),
                ('display', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='WordClass',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=255)),
                ('display_order', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='WordContent',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('content', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(related_name='word_entries_content', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WordEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('relative_url', models.CharField(unique=True, max_length=155)),
                ('word', models.CharField(unique=True, max_length=100)),
                ('short_description', models.CharField(unique=True, max_length=155)),
                ('audio_file', models.CharField(max_length=255, blank=True, null=True)),
                ('phonetics', models.CharField(max_length=255, blank=True, null=True)),
                ('template', models.CharField(default='word-entry-default.html', max_length=50)),
                ('is_published', models.BooleanField(default=False)),
                ('access_count', models.BigIntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(related_name='word_entries', to=settings.AUTH_USER_MODEL)),
                ('languages', models.ManyToManyField(related_name='word_entries', to='dictionary.Language')),
                ('tags', models.ManyToManyField(related_name='tags', to='dictionary.Tag')),
                ('word_classes', models.ManyToManyField(related_name='word_entries', to='dictionary.WordClass')),
                ('word_content', models.ForeignKey(related_name='word_entries', to='dictionary.WordContent')),
                ('words_related', models.ManyToManyField(related_name='word_related_to', to='dictionary.WordEntry')),
            ],
        ),
        migrations.AddField(
            model_name='picture',
            name='word_content',
            field=models.ForeignKey(related_name='pictures', to='dictionary.WordContent'),
        ),
        migrations.AddField(
            model_name='comment',
            name='word_entry',
            field=models.ForeignKey(related_name='word_entry_comments', to='dictionary.WordEntry'),
        ),
    ]
