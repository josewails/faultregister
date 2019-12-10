# Generated by Django 2.1.9 on 2019-07-01 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20190701_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chart',
            name='chart_type',
            field=models.CharField(choices=[('bar_chart', 'Bar Chart'), ('pie_chart', 'Pie Chart'), ('radar_chart', 'Radar Chart'), ('constant_value', 'Constant Value')], max_length=128),
        ),
    ]
