# Generated by Django 3.2.15 on 2022-09-23 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manoti', '0037_auto_20220923_1915'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankentry',
            name='balance',
            field=models.IntegerField(blank=True, null=True, verbose_name='balance'),
        ),
    ]
