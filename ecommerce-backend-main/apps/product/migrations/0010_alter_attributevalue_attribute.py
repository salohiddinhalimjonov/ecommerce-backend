# Generated by Django 4.2.8 on 2024-04-06 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0009_alter_attribute_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attributevalue",
            name="attribute",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="values_hi",
                to="product.attribute",
            ),
        ),
    ]
