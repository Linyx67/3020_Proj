# Generated by Django 4.1.5 on 2023-01-08 05:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hris_app', '0002_logininfo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='logininfo',
            old_name='username',
            new_name='email',
        ),
    ]
