# Generated by Django 3.2.15 on 2022-09-21 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manoti', '0024_auto_20220917_1459'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposal',
            name='status',
        ),
        migrations.RemoveField(
            model_name='purchaseorder',
            name='status',
        ),
        migrations.AddField(
            model_name='proposal',
            name='is_billed',
            field=models.BooleanField(default=False, help_text='Determines if an invoice was created from this commercial invoice', verbose_name='Is the commercial proposal Billed?'),
        ),
        migrations.AddField(
            model_name='proposal',
            name='is_signed',
            field=models.ForeignKey(blank=True, help_text='Determines if this commercial proposal accepted or refused by the customer or prospect', null=True, on_delete=django.db.models.deletion.CASCADE, to='manoti.statuschoices', verbose_name='Set accepted/refused'),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='is_signed',
            field=models.ForeignKey(blank=True, help_text='Determines if this commercial proposal accepted or refused by the customer or prospect', null=True, on_delete=django.db.models.deletion.CASCADE, to='manoti.statuschoices', verbose_name='Set accepted/refused'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='is_validated',
            field=models.BooleanField(default=False, help_text='was this commercial proposal validated?', verbose_name='Is the commercial proposal validated'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='timestamp',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='proposalline',
            name='unit_price',
            field=models.IntegerField(default=1, verbose_name='Unit price'),
        ),
    ]