# Generated by Django 2.0.3 on 2018-05-11 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadmap', '0005_auto_20180510_0943'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtheme',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
