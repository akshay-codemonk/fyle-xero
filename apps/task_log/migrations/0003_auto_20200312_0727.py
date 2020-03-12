# Generated by Django 2.2.8 on 2020-03-12 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_log', '0002_auto_20200118_1107'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasklog',
            name='level',
        ),
        migrations.RemoveField(
            model_name='tasklog',
            name='task',
        ),
        migrations.AddField(
            model_name='tasklog',
            name='status',
            field=models.CharField(blank=True, help_text='Task status', max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='tasklog',
            name='task_id',
            field=models.CharField(help_text='Fyle job reference', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='tasklog',
            name='type',
            field=models.CharField(default='default_type', help_text='Task type', max_length=64),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tasklog',
            name='detail',
            field=models.TextField(blank=True, help_text='Task details', null=True),
        ),
    ]
