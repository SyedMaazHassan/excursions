# Generated by Django 3.0.7 on 2020-06-30 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donationWeb', '0028_auto_20200630_0800'),
    ]

    operations = [
        migrations.AddField(
            model_name='excursions',
            name='excursions_place',
            field=models.CharField(default='Italy', max_length=255),
            preserve_default=False,
        ),
    ]
