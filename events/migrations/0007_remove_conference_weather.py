# Generated by Django 4.2.2 on 2023-06-24 00:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_remove_conference_lan_remove_conference_lon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conference',
            name='weather',
        ),
    ]