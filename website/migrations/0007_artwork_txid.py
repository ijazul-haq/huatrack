# Generated by Django 2.0 on 2018-01-10 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_auto_20180110_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='artwork',
            name='txid',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
