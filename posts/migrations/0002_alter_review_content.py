# Generated by Django 3.2.18 on 2023-05-24 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='content',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
