# Generated by Django 4.1.3 on 2022-11-19 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("buyer", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="buyer",
            name="address",
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]
