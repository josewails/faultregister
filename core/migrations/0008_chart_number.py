# Generated by Django 2.1.9 on 2019-07-01 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20190701_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='chart',
            name='number',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
