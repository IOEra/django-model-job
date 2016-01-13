# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modeljob', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='args',
            field=models.CharField(default=b'[]', max_length=200),
        ),
        migrations.AlterField(
            model_name='task',
            name='kwargs',
            field=models.CharField(default=b'{}', max_length=200),
        ),
    ]
