# Generated by Django 4.1.5 on 2023-01-11 08:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff_app', '0007_alter_awards_options_alter_publications_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='religion',
        ),
    ]
