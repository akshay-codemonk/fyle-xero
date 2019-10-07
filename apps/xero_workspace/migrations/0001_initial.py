# Generated by Django 2.2.4 on 2019-09-10 09:43

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        # ('schedule', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sync_activity', '0001_initial'),
        ('fyle_connect', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workspace',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Name of this workspace', max_length=20)),
                ('employee_contact', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='Fyle Employee email to Xero Contact email mapping', null=True)),
                ('category_account', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='Fyle Category to Xero Account mapping', null=True)),
                ('transform_sql', models.TextField(blank=True, help_text='Transform SQL', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Updated at')),
                ('user', models.ManyToManyField(help_text='Users belonging to this workspace', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='XeroCredential',
            fields=[
                ('id', models.AutoField(help_text='id', primary_key=True, serialize=False)),
                ('pem_file', models.FileField(help_text='Xero pem file', upload_to='')),
                ('consumer_key', models.CharField(help_text='Xero Consumer key', max_length=256)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Updated at')),
                ('workspace', models.ForeignKey(help_text='Workspace', on_delete=django.db.models.deletion.CASCADE, to='xero_workspace.Workspace')),
            ],
        ),
        migrations.CreateModel(
            name='WorkspaceSchedule',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Updated at')),
                ('schedule', models.OneToOneField(help_text='FK to Schedule', on_delete=django.db.models.deletion.CASCADE, to='django_q.Schedule')),
                ('workspace', models.OneToOneField(help_text='FK to Workspace', on_delete=django.db.models.deletion.CASCADE, to='xero_workspace.Workspace')),
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
            name='WorkspaceActivity',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Updated at')),
                ('activity', models.ForeignKey(help_text='FK to Activity', on_delete=django.db.models.deletion.CASCADE, to='sync_activity.Activity')),
                ('workspace', models.ForeignKey(help_text='FK to Workspace', on_delete=django.db.models.deletion.CASCADE, to='xero_workspace.Workspace')),
            ],
            options={
                'unique_together': {('workspace', 'activity')},
            },
        ),
    ]
