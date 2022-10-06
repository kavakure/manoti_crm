# Generated by Django 3.2.15 on 2022-10-04 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manoti', '0053_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='bank_entry',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='manoti.bankentry', verbose_name='Bank Entry'),
        ),
    ]
