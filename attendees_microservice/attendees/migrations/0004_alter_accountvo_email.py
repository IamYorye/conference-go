# Generated by Django 4.2.2 on 2023-06-30 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendees', '0003_remove_accountvo_import_href'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountvo',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
