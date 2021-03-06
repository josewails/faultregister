# Generated by Django 2.1.9 on 2019-07-25 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20190725_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chart',
            name='chart_type',
            field=models.CharField(choices=[('bar_chart', 'Bar Chart'), ('pie_chart', 'Pie Chart'), ('radar_chart', 'Radar Chart'), ('constant_value', 'Constant Value'), ('donut_chart', 'Donut Chart'), ('polar_chart', 'Polar Chart'), ('multiple_statistics', 'Multiple Statistics'), ('product_line', 'Product Line'), ('multiple_bar_chart', 'Multiple Bar Chart'), ('dual_line_chart', 'Dual Line Chart'), ('line_chart', 'Line Chart')], max_length=128),
        ),
    ]
