# Generated by Django 4.1.5 on 2023-01-09 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hris_app', '0005_remove_staffuser_address_staffuser_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffuser',
            name='profile_pic',
            field=models.FileField(upload_to=''),
        ),
    ]
