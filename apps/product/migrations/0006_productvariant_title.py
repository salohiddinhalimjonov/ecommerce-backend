# Generated by Django 4.2.8 on 2024-03-03 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0005_category_level"),
    ]

    operations = [
        migrations.AddField(
            model_name="productvariant",
            name="title",
            field=models.CharField(default="test", max_length=255),
            preserve_default=False,
        ),
    ]
