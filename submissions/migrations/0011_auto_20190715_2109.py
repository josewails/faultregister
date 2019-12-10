# Generated by Django 2.1.10 on 2019-07-15 21:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0010_delete_graph'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='submissions.SubmissionStatus'),
        ),
    ]
