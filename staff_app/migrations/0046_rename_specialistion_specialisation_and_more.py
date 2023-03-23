# Generated by Django 4.1.5 on 2023-03-23 03:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('staff_app', '0045_delete_religion'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Specialistion',
            new_name='Specialisation',
        ),
        migrations.AlterField(
            model_name='research',
            name='interest',
            field=models.CharField(max_length=200, null=True, verbose_name='Interest'),
        ),
        migrations.AlterField(
            model_name='research',
            name='research',
            field=models.CharField(max_length=200, null=True, verbose_name='Research'),
        ),
        migrations.AlterField(
            model_name='supervision',
            name='level',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1, null=True, verbose_name='Degree Level'),
        ),
    ]
