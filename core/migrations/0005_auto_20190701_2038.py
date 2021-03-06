# Generated by Django 2.1.9 on 2019-07-01 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20190701_2025'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chart',
            old_name='name',
            new_name='chart_name',
        ),
        migrations.AddField(
            model_name='chart',
            name='chart_type',
            field=models.CharField(choices=[('bar_chart', 'Bar Chart'), ('pie_chart', 'Pie Chart')], default='bar_chart', max_length=128),
            preserve_default=False,
        ),
    ]
