# Generated by Django 4.0.4 on 2022-05-16 12:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_token'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='token',
            options={'verbose_name': 'Token', 'verbose_name_plural': 'Tokens'},
        ),
        migrations.AlterUniqueTogether(
            name='token',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='token',
            name='name',
        ),
    ]
