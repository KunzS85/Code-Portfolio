# Generated by Django 4.2.4 on 2023-09-16 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("kalender", "0002_rename_closedtimewondow_closedtimewindow"),
    ]

    operations = [
        migrations.CreateModel(
            name="Rule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField()),
            ],
        ),
    ]
