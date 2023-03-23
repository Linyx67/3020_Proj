# Generated by Django 4.1.5 on 2023-03-23 03:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff_app', '0047_alter_specialisation_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='vitae',
            field=models.FileField(blank=True, help_text='upload in .docx or .pdf', null=True, upload_to='vitae/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'docx'])], verbose_name='Cirriculum Vitae'),
        ),
    ]
