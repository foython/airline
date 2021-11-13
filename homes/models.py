from django.db import models
from flight.models import Airport
# Create your models here.


class FlightPackage(models.Model):
    price = models.CharField(max_length=32)
    departure = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='pack_departure')
    arrival = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='pack_arrival')
    description = models.CharField(max_length=128)


class TourPackage(models.Model):
    place = models.CharField(max_length=32)
    hotel = models.CharField(max_length=32)
    duration = models.CharField(max_length=32)
    price = models.CharField(max_length=32)
