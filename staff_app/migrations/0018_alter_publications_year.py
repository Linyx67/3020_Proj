# Generated by Django 4.1.5 on 2023-01-15 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff_app', '0017_alter_employee_nisnumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publications',
            name='year',
            field=models.IntegerField(null=True, verbose_name='Year'),
        ),
    ]