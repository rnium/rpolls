# Generated by Django 3.2.9 on 2022-06-11 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0004_auto_20220612_0157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='added',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated',
            field=models.DateTimeField(),
        ),
    ]
