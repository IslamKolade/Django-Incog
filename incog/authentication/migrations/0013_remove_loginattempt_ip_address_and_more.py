# Generated by Django 4.1.4 on 2022-12-30 22:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0012_loginattempt"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="loginattempt",
            name="ip_address",
        ),
        migrations.RemoveField(
            model_name="loginattempt",
            name="success",
        ),
        migrations.RemoveField(
            model_name="loginattempt",
            name="user_agent",
        ),
        migrations.RemoveField(
            model_name="loginattempt",
            name="username",
        ),
        migrations.AlterField(
            model_name="loginattempt",
            name="timestamp",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
