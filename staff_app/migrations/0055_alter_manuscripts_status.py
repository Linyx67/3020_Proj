# Generated by Django 4.1.5 on 2023-03-28 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff_app', '0054_remove_manuscripts_in_preparation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manuscripts',
            name='status',
            field=models.CharField(choices=[('in preparation', 'in preparation'), ('under review', 'under review')], default='in preparation', max_length=25, null=True, verbose_name='Status'),
        ),
    ]
