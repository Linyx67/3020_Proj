# Generated by Django 4.1.5 on 2023-03-17 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff_app', '0035_remove_consultancies_year_end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultancies',
            name='period',
            field=models.CharField(max_length=50, null=True, verbose_name='Period'),
        ),
        migrations.AlterField(
            model_name='consultancies',
            name='position',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Position'),
        ),
    ]