# Generated by Django 5.1.1 on 2024-10-16 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0006_alter_sellerregistration_seller_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellerregistration',
            name='rejection_detail',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
