# Generated by Django 3.0.8 on 2020-08-21 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0004_auto_20200804_0945"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="nutriments",
            field=models.CharField(default="", max_length=500),
        ),
    ]
