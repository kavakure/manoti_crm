# Generated by Django 3.2.15 on 2022-09-24 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manoti', '0040_rename_bank_bankentryattachedfile_entry'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendorinvoice',
            name='is_paid',
            field=models.BooleanField(default=False, verbose_name='Is paid ?'),
        ),
        migrations.AddField(
            model_name='vendorinvoice',
            name='reference_number',
            field=models.IntegerField(default=1, verbose_name='Reference number'),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='is_private',
            field=models.BooleanField(default=True, help_text='Is this entry private to the the user that added it ?', verbose_name='Is private'),
        ),
        migrations.AlterField(
            model_name='bankentry',
            name='is_private',
            field=models.BooleanField(default=True, help_text='Is this entry private to the the user that added it ?', verbose_name='Is private'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='is_private',
            field=models.BooleanField(default=True, help_text='Is this entry private to the the user that added it ?', verbose_name='Is private'),
        ),
        migrations.AlterField(
            model_name='customerinvoice',
            name='is_private',
            field=models.BooleanField(default=True, help_text='Is this entry private to the the user that added it ?', verbose_name='Is private'),
        ),
        migrations.AlterField(
            model_name='vendorinvoice',
            name='is_private',
            field=models.BooleanField(default=True, help_text='Is this entry private to the the user that added it ?', verbose_name='Is private'),
        ),
    ]
