# Generated by Django 3.1.3 on 2020-11-22 11:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todo',
            old_name='memo',
            new_name='description',
        ),
    ]
