# Generated by Django 4.1.4 on 2022-12-26 09:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "facebook_url",
                    models.CharField(blank=True, max_length=80, null=True),
                ),
                (
                    "instagram_url",
                    models.CharField(blank=True, max_length=80, null=True),
                ),
                (
                    "whatsapp_url",
                    models.CharField(blank=True, max_length=80, null=True),
                ),
                ("bio", models.TextField(blank=True, max_length=150, null=True)),
                ("created", models.DateField(auto_now_add=True)),
                (
                    "profile_picture",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="profile_pictures",
                        verbose_name="Picture",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
