# Generated by Django 2.2.4 on 2020-01-15 10:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0005_auto_20200115_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasklog',
            name='task',
            field=models.ForeignKey(help_text='FK to Django Q Task', on_delete=django.db.models.deletion.PROTECT, to='django_q.Task'),
        ),
    ]
