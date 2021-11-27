from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from .models import TourPackage, FlightPackage
from flight.models import AddFlight, Airport

from django.contrib.auth.decorators import login_required


# Create your views here.


def index(request):
    return render(request, 'index.html', {'fpackage': FlightPackage.objects.all(),
                                          'tpackage': TourPackage.objects.all(),
                                          'airports': Airport.objects.all().order_by('city'),
                                          'range': range(11)
                                          })


def flight(request, fpack_id):
    fpack = FlightPackage.objects.get(pk=fpack_id)
    myflight = AddFlight.objects.all()
    return render(request, 'index1.html', {'fpack': fpack,
                                           'myflight': myflight,
                                           })


@login_required
def book(request, flight_id):
    bflight = AddFlight.objects.get(pk=flight_id)
    return render(request, 'book.html', {'bflight': bflight})


def tour(request, tour_id):
    booked_tour = TourPackage.objects.get(pk=tour_id)
    return render(request, 'tour.html', {'booked_tour': booked_tour})


