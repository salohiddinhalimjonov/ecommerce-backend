# Generated by Django 4.2.8 on 2024-03-27 21:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0007_usermodel_password"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="usermodel",
            name="password",
        ),
    ]
