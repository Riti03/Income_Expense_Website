# Generated by Django 4.1.5 on 2023-03-24 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userincome", "0006_consulting_meetingid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="consulting", name="scheduledat", field=models.DateTimeField(),
        ),
    ]