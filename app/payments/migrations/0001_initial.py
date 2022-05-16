# Generated by Django 4.0.4 on 2022-05-15 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('notification_type', models.CharField(max_length=32)),
                ('operation_id', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('amount', models.FloatField(null=True)),
                ('withdraw_amount', models.FloatField(null=True)),
                ('currency', models.CharField(max_length=8)),
                ('datetime', models.DateTimeField()),
                ('sender', models.CharField(blank=True, max_length=32, null=True)),
                ('label', models.CharField(blank=True, max_length=64, null=True)),
                ('sha1_hash', models.CharField(max_length=128)),
                ('test_notification', models.BooleanField(default=False)),
                ('codepro', models.BooleanField(default=False)),
                ('unaccepted', models.BooleanField(default=False)),
                ('raw_data', models.JSONField(null=True)),
                ('counted', models.BooleanField(default=False)),
            ],
        ),
    ]