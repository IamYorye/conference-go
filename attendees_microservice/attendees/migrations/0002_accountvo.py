# Generated by Django 4.2.2 on 2023-06-30 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendees', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountVO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_href', models.CharField(max_length=200, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=False)),
                ('updated', models.DateField()),
            ],
        ),
    ]