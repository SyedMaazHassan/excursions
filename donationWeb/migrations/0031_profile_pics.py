# Generated by Django 3.0.7 on 2020-07-01 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donationWeb', '0030_user_confirmation'),
    ]

    operations = [
        migrations.CreateModel(
            name='profile_pics',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('user_img', models.ImageField(upload_to='profilePics')),
            ],
        ),
    ]
