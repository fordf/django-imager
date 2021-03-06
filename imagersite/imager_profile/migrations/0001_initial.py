# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-25 03:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagerProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('camera_type', models.CharField(choices=[('IPHONE', 'iPhone'), ('NIKON', 'Nikon'), ('CANNON', 'Cannon'), ('OTHER', 'Other')], max_length=128)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('website', models.CharField(blank=True, max_length=255, null=True)),
                ('hireable', models.BooleanField(default=True)),
                ('travel_radius', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('type_of_photography', models.CharField(choices=[('NATURE', 'Nature'), ('URBAN', 'Urban'), ('PORTRAIT', 'Portrait'), ('OTHER', 'Other')], max_length=144, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
