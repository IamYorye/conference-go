# Generated by Django 4.2.2 on 2023-06-24 00:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_conference_lan_conference_lon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conference',
            name='lan',
        ),
        migrations.RemoveField(
            model_name='conference',
            name='lon',
        ),
    ]
