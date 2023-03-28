# Generated by Django 4.1.5 on 2023-03-28 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff_app', '0056_alter_supervision_firstname_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=125, null=True, verbose_name='Name')),
                ('email', models.EmailField(blank=True, default=None, max_length=255, null=True, verbose_name='Email')),
                ('information', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Information')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
                'ordering': ['-created'],
            },
        ),
    ]