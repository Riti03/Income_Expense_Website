# Generated by Django 4.1.5 on 2023-02-20 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("expense", "0002_auto_20221227_1243"),
    ]

    operations = [
        migrations.AlterModelOptions(name="expense", options={"ordering": ["-date"]},),
    ]
