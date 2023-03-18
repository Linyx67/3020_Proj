# Generated by Django 4.1.5 on 2023-03-17 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff_app', '0036_alter_consultancies_period_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manuscripts',
            name='in_preparation',
            field=models.BooleanField(default=False, verbose_name='In Preparation'),
        ),
        migrations.AlterField(
            model_name='manuscripts',
            name='in_review',
            field=models.BooleanField(default=False, verbose_name='In Review'),
        ),
    ]