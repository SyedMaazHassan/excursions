# Generated by Django 3.0.3 on 2020-07-04 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donationWeb', '0034_booking_details_credit_cards'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credit_cards',
            name='total_credit',
            field=models.FloatField(default=5000),
        ),
    ]
