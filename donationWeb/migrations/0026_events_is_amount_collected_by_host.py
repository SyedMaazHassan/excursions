# Generated by Django 3.0.5 on 2020-06-04 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donationWeb', '0025_events_iscompleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='is_amount_collected_by_host',
            field=models.BooleanField(default=0),
        ),
    ]
