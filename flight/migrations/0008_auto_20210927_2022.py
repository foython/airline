# Generated by Django 3.1.7 on 2021-09-27 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0007_auto_20210927_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booked',
            name='agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agent_booked', to='flight.agent'),
        ),
    ]
