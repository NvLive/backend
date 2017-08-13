# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-13 07:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navalny_live', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PushTokens',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'PushToken',
                'verbose_name_plural': 'PushTokens',
            },
        ),
        migrations.AddField(
            model_name='pushtokens',
            name='shows',
            field=models.ManyToManyField(blank=True, null=True, related_name='shows_push_token', related_query_name='shows_push_token_rel', to='navalny_live.Show'),
        ),
    ]
