# Generated by Django 5.1.3 on 2024-11-16 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_event_suggestions'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='note',
            field=models.TextField(blank=True),
        ),
    ]
