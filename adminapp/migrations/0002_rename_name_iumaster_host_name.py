# Generated by Django 5.1.1 on 2024-10-10 05:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='iumaster',
            old_name='name',
            new_name='host_name',
        ),
    ]
