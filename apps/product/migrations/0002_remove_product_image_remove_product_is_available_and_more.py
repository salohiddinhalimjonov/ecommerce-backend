# Generated by Django 4.2.8 on 2024-02-26 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="image",
        ),
        migrations.RemoveField(
            model_name="product",
            name="is_available",
        ),
        migrations.RemoveField(
            model_name="product",
            name="price",
        ),
        migrations.AddField(
            model_name="productvariant",
            name="is_main",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="category",
            name="image",
            field=models.ImageField(upload_to="product/category/%Y/%m/%d/"),
        ),
        migrations.AlterField(
            model_name="productvariantimage",
            name="image",
            field=models.ImageField(upload_to="product/product_variant/%Y/%m/%d/"),
        ),
    ]
