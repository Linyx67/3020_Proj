# Generated by Django 4.1.5 on 2023-03-23 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff_app', '0050_delete_emergency'),
    ]

    operations = [
        migrations.AddField(
            model_name='requests',
            name='status',
            field=models.CharField(default='pending', max_length=12),
        ),
    ]
