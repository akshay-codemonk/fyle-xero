# Generated by Django 2.2.8 on 2020-01-17 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xero_workspace', '0014_auto_20200116_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeemapping',
            name='employee_email',
            field=models.EmailField(help_text='Email id of the Fyle employee', max_length=255),
        ),
        migrations.AlterField(
            model_name='projectmapping',
            name='project_name',
            field=models.CharField(help_text='Fyle Project Name', max_length=64),
        ),
        migrations.AlterUniqueTogether(
            name='categorymapping',
            unique_together={('category', 'sub_category', 'workspace')},
        ),
        migrations.AlterUniqueTogether(
            name='employeemapping',
            unique_together={('employee_email', 'workspace')},
        ),
        migrations.AlterUniqueTogether(
            name='projectmapping',
            unique_together={('project_name', 'workspace')},
        ),
    ]
