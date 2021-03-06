# Generated by Django 3.0.3 on 2020-07-04 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donationWeb', '0033_auto_20200702_0015'),
    ]

    operations = [
        migrations.CreateModel(
            name='booking_details',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('available_row_id', models.IntegerField()),
                ('total_members', models.IntegerField()),
                ('booked_by', models.IntegerField()),
                ('total_amount', models.FloatField()),
                ('current_date', models.DateField(default='2020-07-04')),
            ],
        ),
        migrations.CreateModel(
            name='credit_cards',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('owner_id', models.IntegerField()),
                ('exp_date', models.DateField()),
                ('cvv_num', models.CharField(max_length=3)),
                ('card_number', models.CharField(max_length=20)),
                ('total_credit', models.IntegerField(default=5000)),
            ],
        ),
    ]
