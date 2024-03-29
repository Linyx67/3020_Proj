# Generated by Django 4.1.5 on 2023-03-28 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff_app', '0058_remove_requests_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requests',
            name='information',
            field=models.CharField(choices=[('Study and Travel Grant', 'Study and Travel Grant'), ('Institutional Visit Allowance', 'Institutional Visit Allowance'), ('Development and Training Grant', 'Development and Training Grant'), ('Book Grant', 'Book Grant'), ('Claim Form', 'Claim Form'), ('Pension Plans', 'Pension Plans'), ('Other', 'Other')], default='Study and Travel Grant', max_length=40, verbose_name='Information'),
        ),
    ]
