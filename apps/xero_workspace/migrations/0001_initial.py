# Generated by Django 2.2.8 on 2020-03-19 15:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fyle_connect', '0001_initial'),
        ('xero_connect', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('invoice_number', models.CharField(help_text='Invoice number', max_length=64)),
                ('invoice_id', models.CharField(blank=True, help_text='Invoice id', max_length=64, null=True)),
                ('contact_name', models.CharField(help_text='Contact Name', max_length=64)),
                ('date', models.DateTimeField(help_text='Invoice created date')),
                ('due_date', models.DateTimeField(blank=True, help_text='Invoice due date', null=True)),
                ('description', models.CharField(help_text='Description', max_length=64)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Updated at')),
            ],
        ),
        migrations.CreateModel(
            name='Workspace',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Name of this workspace', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Updated at')),
                ('user', models.ManyToManyField(help_text='Users belonging to this workspace', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='XeroCredential',
            fields=[
                ('id', models.AutoField(help_text='id', primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Updated at')),
                ('workspace', models.OneToOneField(help_text='Workspace', on_delete=django.db.models.deletion.CASCADE, to='xero_workspace.Workspace')),
                ('xero_auth', models.OneToOneField(help_text='FK to Xero Auth', on_delete=django.db.models.deletion.CASCADE, to='xero_connect.XeroAuth')),
            ],
        ),
        migrations.CreateModel(
            name='WorkspaceSchedule',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('enabled', models.BooleanField(default=False, help_text='Schedule enabled')),
                ('start_datetime', models.DateTimeField(help_text='Datetime for start of schedule', null=True)),
                ('interval_hours', models.IntegerField(help_text='Interval in hours', null=True)),
                ('fyle_job_id', models.CharField(help_text='Fyle job ID', max_length=255, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Updated at')),
                ('workspace', models.OneToOneField(help_text='FK to Workspace', on_delete=django.db.models.deletion.CASCADE, to='xero_workspace.Workspace')),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceLineItem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('account_code', models.IntegerField(help_text='Account Code')),
                ('account_name', models.CharField(help_text='Account name', max_length=64)),
                ('description', models.CharField(help_text='Description', max_length=64)),
                ('amount', models.FloatField(help_text='Invoice line item amount')),
                ('tracking_category_name', models.CharField(blank=True, help_text='Tracking Category Name', max_length=64, null=True)),
                ('tracking_category_option', models.CharField(blank=True, help_text='Tracking Category Option', max_length=64, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Updated at')),
                ('invoice', models.ForeignKey(help_text='FK to Invoice', on_delete=django.db.models.deletion.CASCADE, related_name='invoice_line_items', to='xero_workspace.Invoice')),
            ],
        ),
        migrations.CreateModel(
            name='FyleCredential',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Updated at')),
                ('fyle_auth', models.OneToOneField(help_text='FK to Fyle Auth', on_delete=django.db.models.deletion.CASCADE, to='fyle_connect.FyleAuth')),
                ('workspace', models.OneToOneField(help_text='FK to Workspace', on_delete=django.db.models.deletion.CASCADE, to='xero_workspace.Workspace')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectMapping',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('project_name', models.CharField(help_text='Fyle Project Name', max_length=64)),
                ('tracking_category_name', models.CharField(help_text='Xero Tracking Category Name', max_length=64)),
                ('tracking_category_option', models.CharField(help_text='Xero Tracking Category Option', max_length=64)),
                ('invalid', models.BooleanField(default=False, help_text='Indicates if this mapping is invalid')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Updated at')),
                ('workspace', models.ForeignKey(help_text='Workspace this mapping belongs to', on_delete=django.db.models.deletion.CASCADE, to='xero_workspace.Workspace')),
            ],
            options={
                'ordering': ['-created_at'],
                'unique_together': {('project_name', 'workspace')},
            },
        ),
        migrations.CreateModel(
            name='EmployeeMapping',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('employee_email', models.EmailField(help_text='Email id of the Fyle employee', max_length=255)),
                ('contact_name', models.CharField(help_text='Name of the Xero contact', max_length=255)),
                ('invalid', models.BooleanField(default=False, help_text='Indicates if this mapping is invalid')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Updated at')),
                ('workspace', models.ForeignKey(help_text='Workspace this mapping belongs to', on_delete=django.db.models.deletion.CASCADE, to='xero_workspace.Workspace')),
            ],
            options={
                'ordering': ['-created_at'],
                'unique_together': {('employee_email', 'workspace')},
            },
        ),
        migrations.CreateModel(
            name='CategoryMapping',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('category', models.CharField(help_text='Fyle Expense Category', max_length=64)),
                ('sub_category', models.CharField(default='Unspecified', help_text='Fyle Expense Sub-Category', max_length=64, null=True)),
                ('account_code', models.IntegerField(blank=True, help_text='Xero Account code', null=True)),
                ('invalid', models.BooleanField(default=False, help_text='Indicates if this mapping is invalid')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Updated at')),
                ('workspace', models.ForeignKey(help_text='Workspace this mapping belongs to', on_delete=django.db.models.deletion.CASCADE, to='xero_workspace.Workspace')),
            ],
            options={
                'ordering': ['-created_at'],
                'unique_together': {('category', 'sub_category', 'workspace')},
            },
        ),
    ]
