# Generated by Django 3.0.5 on 2020-06-04 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donationWeb', '0023_donation_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='remaining_amount',
            field=models.IntegerField(default=0),
        ),
    ]
