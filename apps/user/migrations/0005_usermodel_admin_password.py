# Generated by Django 4.2.8 on 2024-02-16 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0004_remove_usermodel_password"),
    ]

    operations = [
        migrations.AddField(
            model_name="usermodel",
            name="admin_password",
            field=models.CharField(blank=True, max_length=32),
        ),
    ]