# Generated by Django 4.1.4 on 2023-02-19 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inbox_messages", "0014_alter_inboxes_vid_img_poster"),
    ]

    operations = [
        migrations.AlterField(
            model_name="inboxes",
            name="vid_img_poster",
            field=models.CharField(
                blank=True,
                default="core/static/images/logo.png",
                max_length=100,
                null=True,
            ),
        ),
    ]
