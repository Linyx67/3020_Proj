# Generated by Django 4.1.5 on 2023-03-17 04:10

import django.core.validators
from django.db import migrations, models
import staff_app.validate


class Migration(migrations.Migration):

    dependencies = [
        ('staff_app', '0034_remove_consultancies_period_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consultancies',
            name='year_end',
        ),
        migrations.RemoveField(
            model_name='consultancies',
            name='year_start',
        ),
        migrations.AddField(
            model_name='consultancies',
            name='period',
            field=models.IntegerField(null=True, verbose_name='Period'),
        ),
        migrations.AlterField(
            model_name='development',
            name='year_end',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1900), staff_app.validate.max_value_current_year], verbose_name='End Year'),
        ),
        migrations.AlterField(
            model_name='development',
            name='year_start',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1900), staff_app.validate.max_value_current_year], verbose_name='Start Year'),
        ),
    ]