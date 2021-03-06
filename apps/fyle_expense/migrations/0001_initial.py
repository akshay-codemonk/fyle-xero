# Generated by Django 2.2.8 on 2020-03-19 15:19

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('employee_email', models.EmailField(help_text='Email id of the Fyle employee', max_length=255)),
                ('category', models.CharField(blank=True, help_text='Fyle Expense Category', max_length=64, null=True)),
                ('sub_category', models.CharField(blank=True, help_text='Fyle Expense Sub-Category', max_length=64, null=True)),
                ('vendor', models.CharField(blank=True, help_text='Vendor', max_length=64, null=True)),
                ('purpose', models.CharField(blank=True, help_text='Purpose', max_length=64, null=True)),
                ('expense_id', models.CharField(help_text='Expense ID', max_length=64, unique=True)),
                ('expense_number', models.CharField(help_text='Expense Number', max_length=64)),
                ('amount', models.FloatField(help_text='Amount')),
                ('settlement_id', models.CharField(help_text='Settlement ID', max_length=64)),
                ('report_id', models.CharField(help_text='Report ID', max_length=64)),
                ('project', models.CharField(blank=True, help_text='Project', max_length=64, null=True)),
                ('expense_created_at', models.DateTimeField(help_text='Expense created at')),
                ('spent_at', models.DateTimeField(help_text='Expense spent at')),
                ('reimbursable', models.BooleanField(help_text='Expense reimbursable or not')),
                ('state', models.CharField(help_text='Expense state', max_length=64)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Updated at')),
            ],
            options={
                'ordering': ['-created_at'],
                'get_latest_by': 'created_at',
            },
        ),
        migrations.CreateModel(
            name='ExpenseGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('description', django.contrib.postgres.fields.jsonb.JSONField(default=dict, help_text='Description')),
                ('status', models.CharField(help_text='Status', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Updated at')),
                ('expenses', models.ManyToManyField(help_text='Expenses under this Expense Group', to='fyle_expense.Expense')),
            ],
            options={
                'ordering': ['-created_at'],
                'get_latest_by': 'created_at',
            },
        ),
    ]
