# Generated by Django 2.1.9 on 2019-07-01 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0002_delete_cachedsubmissionids'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('graph_slug', models.CharField(max_length=256)),
                ('graph_end_point', models.CharField(max_length=64)),
            ],
        ),
    ]
