# Generated by Django 4.2.4 on 2023-10-19 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("alp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="informationdetail",
            name="images",
            field=models.ManyToManyField(blank=True, to="alp.picture"),
        ),
        migrations.AlterField(
            model_name="informationdetail",
            name="videos",
            field=models.ManyToManyField(blank=True, to="alp.video"),
        ),
    ]