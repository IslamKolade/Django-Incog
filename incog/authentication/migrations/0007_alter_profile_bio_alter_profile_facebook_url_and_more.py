# Generated by Django 4.1.4 on 2022-12-27 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0006_alter_profile_profile_picture"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="bio",
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="facebook_url",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="instagram_url",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="whatsapp_url",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]