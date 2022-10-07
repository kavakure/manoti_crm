# Generated by Django 3.2.15 on 2022-09-23 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manoti', '0029_remove_bankaccount_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankaccount',
            name='accounting_account',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Accounting account'),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='business',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manoti.business', verbose_name='Business'),
        ),
    ]