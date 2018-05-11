# Generated by Django 2.0.3 on 2018-05-10 07:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('roadmap', '0004_auto_20180510_0659'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemComment',
            fields=[
                ('uid', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_comment_author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['-created_date']},
        ),
        migrations.AddField(
            model_name='itemcomment',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_comment_item', to='roadmap.Item'),
        ),
    ]
