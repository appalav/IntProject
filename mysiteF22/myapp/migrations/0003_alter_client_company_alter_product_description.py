# Generated by Django 4.1.2 on 2022-10-17 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0002_category_warehouse_product_description_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="company",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
    ]
