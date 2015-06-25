# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('django_comments', '0002_update_user_email_field_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='TComment',
            fields=[
                ('comment_ptr', models.OneToOneField(to='django_comments.Comment', serialize=False, parent_link=True, auto_created=True, primary_key=True)),
                ('title', models.TextField(blank=True, verbose_name='Title')),
            ],
            options={
                'verbose_name_plural': 'Comments (threaded)',
                'verbose_name': 'Comment (threaded)',
            },
            bases=('django_comments.comment',),
        ),
        migrations.CreateModel(
            name='TCommentNode',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('path', models.CharField(max_length=255, unique=True)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('insertion_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date/time inserted')),
                ('comment', models.OneToOneField(to='bearded_comments.TComment', related_name='node')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
