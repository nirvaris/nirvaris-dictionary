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
                ('author', models.ForeignKey(related_name='word_entry_comments', to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=70)),
                ('location', models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='MetaTag',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=70)),
                ('property', models.CharField(max_length=70)),
                ('content', models.CharField(max_length=70)),
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
            name='PortugueseTerm',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('display_order', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(unique=True, max_length=10)),
                ('display', models.CharField(max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='WordEntry',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('relative_url', models.CharField(unique=True, max_length=155)),
                ('word', models.CharField(max_length=100)),
                ('short_description', models.CharField(max_length=155)),
                ('scientific_name', models.CharField(null=True, blank=True, max_length=255)),
                ('audio_file', models.CharField(null=True, blank=True, max_length=255)),
                ('phonetics', models.CharField(null=True, blank=True, max_length=255)),
                ('meaning', models.TextField()),
                ('curiosities', models.TextField(blank=True)),
                ('template', models.CharField(max_length=50, default='word-entry-default.html')),
                ('is_published', models.BooleanField(default=False)),
                ('access_count', models.BigIntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(related_name='word_entries', to=settings.AUTH_USER_MODEL)),
                ('languages', models.ManyToManyField(related_name='word_entries', to='dictionary.Language')),
                ('tags', models.ManyToManyField(related_name='tags', to='dictionary.Tag')),
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
            model_name='portugueseterm',
            name='word_entry',
            field=models.ForeignKey(related_name='portuguese_terms', to='dictionary.WordEntry'),
        ),
        migrations.AddField(
            model_name='picture',
            name='word_entry',
            field=models.ForeignKey(related_name='pictures', to='dictionary.WordEntry'),
        ),
        migrations.AddField(
            model_name='metatag',
            name='word_entry',
            field=models.ForeignKey(related_name='meta_tags', to='dictionary.WordEntry'),
        ),
        migrations.AddField(
            model_name='comment',
            name='word_entry',
            field=models.ForeignKey(related_name='word_entry_comments', to='dictionary.WordEntry'),
        ),
    ]
