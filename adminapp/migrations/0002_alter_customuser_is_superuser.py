# Generated by Django 5.1.1 on 2024-10-03 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
    ]
