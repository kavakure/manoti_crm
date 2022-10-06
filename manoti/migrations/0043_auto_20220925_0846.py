# Generated by Django 3.2.15 on 2022-09-25 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manoti', '0042_proposal_is_private'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vendorinvoice',
            options={'ordering': ('date',), 'verbose_name': 'Vendor Invoice', 'verbose_name_plural': 'Vendor Invoices'},
        ),
        migrations.AddField(
            model_name='vendorinvoiceline',
            name='total_tax_excl',
            field=models.IntegerField(blank=True, default=0, verbose_name='Total (Tax excl.)'),
        ),
        migrations.AddField(
            model_name='vendorinvoiceline',
            name='total_tax_incl',
            field=models.IntegerField(blank=True, default=0, verbose_name='Total (Tax incl.)'),
        ),
        migrations.AlterField(
            model_name='vendorinvoice',
            name='reference',
            field=models.CharField(default='Draft', max_length=200, unique=True, verbose_name='Internal Reference'),
        ),
        migrations.AlterField(
            model_name='vendorinvoice',
            name='total_payment',
            field=models.IntegerField(default=0, verbose_name='Total payment'),
        ),
    ]
