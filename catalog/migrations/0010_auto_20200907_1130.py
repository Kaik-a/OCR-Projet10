# Generated by Django 3.0.8 on 2020-09-07 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0009_auto_20200824_1209"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="category_tags",
            new_name="categories_tags",
        ),
        migrations.RenameField(
            model_name="product",
            old_name="url_img",
            new_name="image_url",
        ),
    ]
