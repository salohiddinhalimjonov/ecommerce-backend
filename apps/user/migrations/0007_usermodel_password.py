# Generated by Django 4.2.8 on 2024-03-27 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0006_alter_usermodel_admin_password"),
    ]

    operations = [
        migrations.AddField(
            model_name="usermodel",
            name="password",
            field=models.CharField(
                default="AB8187295ab", max_length=128, verbose_name="password"
            ),
            preserve_default=False,
        ),
    ]
