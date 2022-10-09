# Generated by Django 3.2.15 on 2022-09-05 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manoti', '0007_alter_thirdparty_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='thirdparty',
            name='google_map',
            field=models.TextField(blank=True, help_text='Google Map URL of the Third party', null=True, verbose_name='Google Map URL'),
        ),
        migrations.AlterField(
            model_name='thirdparty',
            name='address',
            field=models.TextField(blank=True, help_text='The full address of the Third party', null=True, verbose_name='Full address'),
        ),
        migrations.AlterField(
            model_name='thirdparty',
            name='business_entity_type',
            field=models.ForeignKey(blank=True, help_text='You can change values from this list from the Setup >> Dictionnaries', null=True, on_delete=django.db.models.deletion.CASCADE, to='manoti.businessentitytype', verbose_name='Business entity type'),
        ),
        migrations.AlterField(
            model_name='thirdparty',
            name='third_party_type',
            field=models.ForeignKey(blank=True, help_text='You can change values from this list from the Setup >> Dictionnaries', null=True, on_delete=django.db.models.deletion.CASCADE, to='manoti.thirdpartytype', verbose_name='Third-party type'),
        ),
    ]
