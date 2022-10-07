# Generated by Django 3.2.15 on 2022-09-15 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manoti', '0017_auto_20220914_1851'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankaccount',
            name='balance',
            field=models.IntegerField(default=0, verbose_name='Balance'),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='initial_balance',
            field=models.IntegerField(default=0, verbose_name='Initial balance'),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='minimum_allowed_balance',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Minimum allowed balance'),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='minimum_desired_balance',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Minimum desired balance'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='customer_reference',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Customer reference'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='delivery_date',
            field=models.DateField(blank=True, null=True, verbose_name='Delivery date'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='manoti.statuschoices', verbose_name='Set accepted/refused'),
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(default='Draft', max_length=200, verbose_name='Reference')),
                ('third_party', models.BooleanField(default=False, verbose_name='Vendor ?')),
                ('timestamp', models.DateField(auto_now_add=True, null=True, verbose_name='Date')),
                ('delivery_date', models.DateField(blank=True, null=True, verbose_name='Delivery date')),
                ('note_private', models.TextField(blank=True, null=True, verbose_name='Private note')),
                ('note_public', models.TextField(blank=True, null=True, verbose_name='Public Note')),
                ('amount_excl_tax', models.IntegerField(default=0, verbose_name='Amount (excl. tax)')),
                ('tax', models.IntegerField(default=0, verbose_name='Amount tax')),
                ('amount_incl_tax', models.IntegerField(default=0, verbose_name='Amount (inc. tax)')),
                ('is_validated', models.BooleanField(default=False, help_text='Are you sure you want to validate this commercial proposal under name PR########?', verbose_name='Is the commercial proposal validated')),
                ('document_template', models.ForeignKey(blank=True, help_text='You can change values from this list from the Setup >> Dictionnaries', null=True, on_delete=django.db.models.deletion.CASCADE, to='manoti.proposaldocumenttemplate', verbose_name='Default doc template')),
                ('payment_terms', models.ForeignKey(blank=True, help_text='You can change values from this list from the Setup >> Dictionnaries', null=True, on_delete=django.db.models.deletion.CASCADE, to='manoti.paymentterms', verbose_name='Payment terms')),
                ('payment_type', models.ForeignKey(blank=True, help_text='You can change values from this list from the Setup >> Dictionnaries', null=True, on_delete=django.db.models.deletion.CASCADE, to='manoti.paymenttype', verbose_name='Payment method')),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='manoti.statuschoices', verbose_name='Set accepted/refused')),
                ('vendor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='manoti.thirdparty', verbose_name='Third party')),
            ],
            options={
                'verbose_name': 'Purchase order',
                'verbose_name_plural': 'Purchase orders',
                'ordering': ('timestamp',),
            },
        ),
    ]