# Generated by Django 4.2.7 on 2023-11-22 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alp', '0005_informationdetail_secure'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'verbose_name_plural': 'Kontakte'},
        ),
        migrations.AlterModelOptions(
            name='informationdetail',
            options={'verbose_name_plural': 'Informationen'},
        ),
        migrations.AlterModelOptions(
            name='picture',
            options={'verbose_name_plural': 'Bilder'},
        ),
        migrations.AlterModelOptions(
            name='video',
            options={'verbose_name_plural': 'Videos'},
        ),
    ]
