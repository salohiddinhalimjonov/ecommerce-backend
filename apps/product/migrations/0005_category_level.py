# Generated by Django 4.2.8 on 2024-02-27 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0004_brannd"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="level",
            field=models.IntegerField(default=1),
        ),
    ]
