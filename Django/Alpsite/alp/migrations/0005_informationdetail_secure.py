# Generated by Django 4.2.4 on 2023-10-28 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("alp", "0004_contact_alter_picture_is_gallery_picture"),
    ]

    operations = [
        migrations.AddField(
            model_name="informationdetail",
            name="secure",
            field=models.BooleanField(default=False),
        ),
    ]
