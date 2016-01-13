# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('signal_type', models.CharField(max_length=35, choices=[(b'pre_save', b'Pre-Save'), (b'post_save', b'Post-Save')])),
                ('app_name', models.CharField(max_length=35)),
                ('model_name', models.CharField(max_length=35)),
            ],
        ),
        migrations.CreateModel(
            name='JobRule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=35)),
                ('condition', models.CharField(max_length=210)),
                ('priority', models.SmallIntegerField()),
                ('model_job', models.ForeignKey(related_name='rules', to='modeljob.Job')),
                ('parent', models.ForeignKey(related_name='children', blank=True, to='modeljob.JobRule', null=True)),
            ],
            options={
                'ordering': ['priority'],
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('func', models.CharField(max_length=100)),
                ('args', models.CharField(max_length=200, blank=True)),
                ('kwargs', models.CharField(max_length=200, blank=True)),
                ('timeout', models.PositiveSmallIntegerField(default=180)),
                ('order', models.IntegerField(default=0)),
                ('job', models.ForeignKey(related_name='tasks', to='modeljob.Job')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
