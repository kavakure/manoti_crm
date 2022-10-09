# Generated by Django 3.2.15 on 2022-09-05 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manoti', '0008_auto_20220905_1129'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='proposal',
            options={'ordering': ('timestamp',), 'verbose_name': 'Commercial proposal', 'verbose_name_plural': 'Commercial proposals'},
        ),
        migrations.AlterModelOptions(
            name='thirdparty',
            options={'verbose_name': 'Third party', 'verbose_name_plural': 'Third parties'},
        ),
        migrations.AddField(
            model_name='thirdparty',
            name='is_vendor',
            field=models.BooleanField(default=False, verbose_name='Vendor ?'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='amount_excl_tax',
            field=models.IntegerField(default=0, verbose_name='Amount (excl. tax)'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='amount_incl_tax',
            field=models.IntegerField(default=0, verbose_name='Amount (inc. tax)'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='availability_delay',
            field=models.ForeignKey(blank=True, help_text='You can change values from this list from the Setup >> Dictionnaries', null=True, on_delete=django.db.models.deletion.CASCADE, to='manoti.availabilitydelay', verbose_name='Availability delay (after order)'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='customer_reference',
            field=models.CharField(max_length=200, null=True, verbose_name='Customer reference'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='document_template',
            field=models.ForeignKey(blank=True, help_text='You can change values from this list from the Setup >> Dictionnaries', null=True, on_delete=django.db.models.deletion.CASCADE, to='manoti.proposaldocumenttemplate', verbose_name='Default doc template'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='payment_terms',
            field=models.ForeignKey(blank=True, help_text='You can change values from this list from the Setup >> Dictionnaries', null=True, on_delete=django.db.models.deletion.CASCADE, to='manoti.paymentterms', verbose_name='Payment terms'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='payment_type',
            field=models.ForeignKey(blank=True, help_text='You can change values from this list from the Setup >> Dictionnaries', null=True, on_delete=django.db.models.deletion.CASCADE, to='manoti.paymenttype', verbose_name='Payment method'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='shipping_metod',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='manoti.shippingmetod', verbose_name='Shipping Method'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='source',
            field=models.ForeignKey(blank=True, help_text='You can change values from this list from the Setup >> Dictionnaries', null=True, on_delete=django.db.models.deletion.CASCADE, to='manoti.source', verbose_name='Source'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='tax',
            field=models.IntegerField(default=0, verbose_name='Amount tax'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='timestamp',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='validity_duration',
            field=models.IntegerField(blank=True, default=30, help_text='days', null=True, verbose_name='Validity duration'),
        ),
        migrations.AlterField(
            model_name='thirdparty',
            name='status',
            field=models.CharField(choices=[('open', 'Open'), ('closed', 'Closed')], default='open', max_length=200, verbose_name='Status'),
        ),
    ]
