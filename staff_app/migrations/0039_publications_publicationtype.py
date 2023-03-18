# Generated by Django 4.1.5 on 2023-03-18 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff_app', '0038_grants'),
    ]

    operations = [
        migrations.AddField(
            model_name='publications',
            name='publicationtype',
            field=models.CharField(choices=[('Peer Reviewed Journal', 'Peer Reviewed Journal'), ('Conference Paper', 'Conference Paper'), ('Book', 'Book')], default='Peer Reviewed Journal', max_length=25, null=True, verbose_name='Publication Type'),
        ),
    ]
