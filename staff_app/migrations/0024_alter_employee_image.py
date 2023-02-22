# Generated by Django 4.1.5 on 2023-02-22 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff_app', '0023_alter_employee_image_alter_employee_vitae'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='image',
            field=models.ImageField(blank=True, default='profiles/default.png', help_text='upload image size less than 2.0MB', null=True, upload_to='profiles/', verbose_name='Profile Image'),
        ),
    ]
