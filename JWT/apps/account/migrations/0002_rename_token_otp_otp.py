# Generated by Django 4.2.2 on 2023-06-12 13:11

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="otp",
            old_name="token",
            new_name="otp",
        ),
    ]
