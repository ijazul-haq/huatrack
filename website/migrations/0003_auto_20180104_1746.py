# Generated by Django 2.0 on 2018-01-04 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20180103_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artwork',
            name='path',
            field=models.ImageField(blank=True, null=True, upload_to='artwork', verbose_name='file'),
        ),
    ]