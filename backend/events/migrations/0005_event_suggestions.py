# Generated by Django 5.1.3 on 2024-11-16 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_eventsgroup_remove_event_use_llm_event_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='suggestions',
            field=models.TextField(blank=True),
        ),
    ]
