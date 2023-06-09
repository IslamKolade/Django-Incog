# Generated by Django 4.1.4 on 2023-03-04 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inbox_messages", "0018_remove_inboxes_vid_duration"),
    ]

    operations = [
        migrations.AddField(
            model_name="chat",
            name="recipient_left_chat",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="chat",
            name="sender_left_chat",
            field=models.BooleanField(default=False),
        ),
    ]
