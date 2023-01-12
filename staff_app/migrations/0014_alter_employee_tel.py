# Generated by Django 4.1.5 on 2023-01-12 07:48

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('staff_app', '0013_alter_employee_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='tel',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Phone Number'),
        ),
    ]
