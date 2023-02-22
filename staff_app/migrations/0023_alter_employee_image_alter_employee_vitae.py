# Generated by Django 4.1.5 on 2023-02-22 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff_app', '0022_alter_employee_vitae'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='image',
            field=models.ImageField(blank=True, default='default.png', help_text='upload image size less than 2.0MB', null=True, upload_to='profiles/', verbose_name='Profile Image'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='vitae',
            field=models.FileField(blank=True, help_text='upload in .docx or .pdf', null=True, upload_to='vitae/', verbose_name='Cirriculum Vitae'),
        ),
    ]
