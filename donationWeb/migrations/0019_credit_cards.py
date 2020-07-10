# Generated by Django 3.0.5 on 2020-05-30 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donationWeb', '0018_more_info_is_credit_card_added'),
    ]

    operations = [
        migrations.CreateModel(
            name='credit_cards',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('owner_id', models.IntegerField()),
                ('owner_name', models.CharField(max_length=60)),
                ('owner_surname', models.CharField(max_length=60)),
                ('exp_date', models.DateField()),
                ('cvv_num', models.CharField(max_length=3)),
                ('card_number', models.CharField(max_length=13)),
            ],
        ),
    ]
