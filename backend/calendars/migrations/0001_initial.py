# Generated by Django 5.1.3 on 2024-11-07 16:17

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalendarProvider',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(choices=[('google', 'Google Calendar'), ('outlook', 'Outlook Calendar'), ('apple', 'Apple Calendar')], max_length=50)),
                ('is_connected', models.BooleanField(default=False)),
                ('last_synced', models.DateTimeField(blank=True, null=True)),
                ('credentials', models.JSONField(blank=True, default=dict)),
                ('settings', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='UserPreference',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('key', models.CharField(max_length=50, unique=True)),
                ('value', models.JSONField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventSync',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider_event_id', models.CharField(max_length=255)),
                ('last_synced', models.DateTimeField(auto_now=True)),
                ('sync_status', models.CharField(default='pending', max_length=50)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='syncs', to='events.event')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calendars.calendarprovider')),
            ],
            options={
                'ordering': ['-last_synced'],
                'unique_together': {('event', 'provider')},
            },
        ),
    ]
