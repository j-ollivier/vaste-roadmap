# Generated by Django 2.0.3 on 2018-05-11 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadmap', '0009_auto_20180511_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventlog',
            name='action',
            field=models.CharField(max_length=200),
        ),
    ]
