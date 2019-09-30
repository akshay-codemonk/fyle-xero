# Generated by Django 2.2.4 on 2019-09-30 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xero_workspace', '0007_auto_20190920_1001'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='xerocredential',
            name='file_id',
        ),
        migrations.AddField(
            model_name='xerocredential',
            name='private_key',
            field=models.TextField(default='', help_text='Xero Application Private Key'),
            preserve_default=False,
        ),
    ]
