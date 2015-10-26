# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0002_portugueseterms'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PortugueseTerms',
            new_name='PortugueseTerm',
        ),
    ]
