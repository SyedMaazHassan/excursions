# Generated by Django 3.0.5 on 2020-05-31 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donationWeb', '0021_events'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='target_amount',
            field=models.IntegerField(),
        ),
    ]
