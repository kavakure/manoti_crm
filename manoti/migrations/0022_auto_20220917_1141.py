# Generated by Django 3.2.15 on 2022-09-17 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manoti', '0021_auto_20220916_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='reference_number',
            field=models.IntegerField(default=1, verbose_name='Reference number'),
        ),
        migrations.AlterField(
            model_name='proposalline',
            name='discount',
            field=models.IntegerField(blank=True, default=0, verbose_name='Discount'),
        ),
        migrations.AlterField(
            model_name='proposalline',
            name='proposal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='manoti.proposal', verbose_name='Proposal'),
        ),
        migrations.AlterField(
            model_name='proposalline',
            name='sales_tax',
            field=models.IntegerField(blank=True, null=True, verbose_name='Sales tax'),
        ),
        migrations.AlterField(
            model_name='proposalline',
            name='total_tax_excl',
            field=models.IntegerField(blank=True, default=0, verbose_name='Total (Tax excl.)'),
        ),
        migrations.AlterField(
            model_name='proposalline',
            name='total_tax_incl',
            field=models.IntegerField(blank=True, default=0, verbose_name='Total (Tax incl.)'),
        ),
    ]