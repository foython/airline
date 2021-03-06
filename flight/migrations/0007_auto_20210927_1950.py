# Generated by Django 3.1.7 on 2021-09-27 13:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0006_auto_20210927_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='booked',
            name='return_flight',
            field=models.BooleanField(default=False),
        ),
        migrations.RemoveField(
            model_name='booked',
            name='agent',
        ),
        migrations.AddField(
            model_name='booked',
            name='agent',
            field=models.ForeignKey(blank=True, default=0, on_delete=django.db.models.deletion.CASCADE, related_name='agent_booked', to='flight.agent'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='booked',
            name='flight',
        ),
        migrations.AddField(
            model_name='booked',
            name='flight',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='flight_boooked', to='flight.addflight'),
            preserve_default=False,
        ),
    ]
