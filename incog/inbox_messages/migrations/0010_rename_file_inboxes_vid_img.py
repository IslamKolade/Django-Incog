# Generated by Django 4.1.4 on 2023-02-11 18:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("inbox_messages", "0009_inboxes_file"),
    ]

    operations = [
        migrations.RenameField(
            model_name="inboxes",
            old_name="file",
            new_name="vid_img",
        ),
    ]
