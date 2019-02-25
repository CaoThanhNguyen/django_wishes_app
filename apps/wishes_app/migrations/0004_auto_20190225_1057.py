# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-02-25 16:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0001_initial'),
        ('wishes_app', '0003_auto_20190225_1051'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='login_app.User')),
            ],
        ),
        migrations.RemoveField(
            model_name='wish',
            name='likes',
        ),
        migrations.AddField(
            model_name='like',
            name='wish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='wishes_app.Wish'),
        ),
    ]