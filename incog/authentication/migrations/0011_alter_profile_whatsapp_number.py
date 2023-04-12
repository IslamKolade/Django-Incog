# Generated by Django 4.1.4 on 2022-12-28 14:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0010_remove_profile_instagram_url_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="whatsapp_number",
            field=models.CharField(
                blank=True,
                max_length=15,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
                        regex="^\\+?1?\\d{9,15}$",
                    )
                ],
            ),
        ),
    ]
