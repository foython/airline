from django.shortcuts import render, HttpResponseRedirect
from .models import AddFlight, Booked, Price
from django.urls import reverse
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from datetime import date, timedelta
from homes.models import TourPackage


def all_flight(request):
    return render(request, 'flights.html', {'flight': AddFlight.objects.all()})


def flight(request, flight_id):
    flights = AddFlight.objects.get(pk=flight_id)
    all_date = []
    start_date = date.today()
    end_date = start_date + timedelta(30)
    delta = timedelta(days=1)
    while start_date <= end_date:
        all_date.append(start_date)
        start_date += delta

    return render(request, 'flight.html', {
        'flights': flights,
        'passengers': flights.passengers.all(),
        'all_date': all_date,
        'tour_pack': TourPackage.objects.all()
    })


def search(request):
    if request.method == 'POST':
        round_trip = False
        trip_type = request.POST['ftype']
        arrive_date = None

        if trip_type == 'round':
            round_trip = True
            arrive_date = request.POST.get('arriving')
        depart_date = request.POST.get('departing')
        origin = request.POST.get('origin')
        destination = request.POST.get('destination')
        adult_sit = int(request.POST.get('adult_sit'))
        child_sit = int(request.POST.get('child_sit'))

        global asit

        def asit():
            return adult_sit, child_sit

        dflight = Price.objects.filter(flight__date=depart_date, flight__origin__city=origin,
                                       flight__destination__city=destination)
        aflight = Price.objects.filter(flight__date=arrive_date, flight__origin__city=destination,
                                       flight__destination__city=origin)
        return render(request, 'search.html', {'dflight': dflight, 'aflight': aflight, 'round_trip': round_trip})


def returnbook(request):
    adult_sit, child_sit = asit()
    if request.method == "POST":
        depart_flight = AddFlight.objects.get(pk=request.POST['dflight'])
        depart_price = int(request.POST['price'])

        r = request.POST.get('rflight', False)
        if not r:
            return_flight = False
        else:
            return_flight = AddFlight.objects.get(pk=r)

        return_price = int(request.POST.get('rprice', False))
        depart_child_sit_price = (depart_price // 2) * child_sit
        return_child_sit_price = (return_price // 2) * child_sit
        total_depart = depart_price * adult_sit + depart_child_sit_price
        total_return = return_price * adult_sit + return_child_sit_price
        total = total_depart + total_return
        depart_sit_class = Price.objects.get(flight__id=depart_flight.id)

        depart_sit_type = None

        if depart_sit_class.saver == depart_price:
            depart_sit_type = 'saver'
        elif depart_sit_class.economy == depart_price:
            depart_sit_type = 'economy'
        else:
            depart_sit_type = 'business'

        return_sit_type = None

        if return_flight is not False:
            return_sit_class = Price.objects.get(flight__id=return_flight.id)
            if return_sit_class.saver == return_price:
                return_sit_type = 'saver'
            elif return_sit_class.economy == return_price:
                return_sit_type = 'economy'
            else:
                return_sit_type = 'business'

            global others

        def others():
            return depart_flight, return_flight, total_depart, total_return, depart_sit_type, return_sit_type, \
                   return_flight

        return render(request, 'book.html', {'depart_flight': depart_flight,
                                             'depart_price': depart_price,
                                             'return_flight': return_flight,
                                             'return_price': return_price,
                                             'total_depart': total_depart,
                                             'total_return': total_return,
                                             'adult_sit': adult_sit,
                                             'child_sit': child_sit,
                                             'total': total,
                                             'depart_child_sit_price': depart_child_sit_price,
                                             'return_child_sit_price': return_child_sit_price,
                                             'depart_sit_type': depart_sit_type,
                                             'return_sit_type': return_sit_type
                                             })


def con_booked(request):
    adult_sit, child_sit = asit()
    depart_flight, return_flight, total_depart, total_return, depart_sit_type, return_sit_type, return_flight = others()
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        contact_no = request.POST['contact_no']

        booked = Booked(first_name=first_name, last_name=last_name, email=email, contact_no=contact_no,
                        flight=depart_flight, no_of_adult_sit=adult_sit, no_of_child_sit=child_sit,
                        sit_type=depart_sit_type, total_amount=total_depart)
        booked.save()
        rbooked = None
        if return_flight:
            return_type = True
            rbooked = Booked(first_name=first_name, last_name=last_name, email=email, contact_no=contact_no,
                             flight=return_flight, no_of_adult_sit=adult_sit, no_of_child_sit=child_sit,
                             sit_type=return_sit_type, total_amount=total_return, return_flight=return_type)
            rbooked.save()
        #else:
            #return HttpResponseRedirect(reverse('confirm'))
        global confirms

        def confirms():
            return booked, rbooked

        return HttpResponseRedirect(reverse('confirm'))


def confirm(request):
    booked, rbooked = confirms()
    return render(request, 'confirm.html', {'booked': booked, 'rbooked': rbooked})



def print(request):
    booked, rbooked = confirms()
    d = str(booked)
    r = str(rbooked)
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter, bottomup=0)
    pdf.setFont('Helvetica', 30)
    pdf.setFillColorRGB(0, 0, 255)
    pdf.drawCentredString(300, 50, 'Confirmation')
    pdf.setFont('Helvetica', 20)
    pdf.drawString(40, 100, 'Departure:')
    text = pdf.beginText(40, 120)
    text.setFont('Helvetica', 9)
    text.textLine(d)
    pdf.drawText(text)
    pdf.setFont('Helvetica', 20)
    pdf.drawString(40, 150, 'Return:')
    text1 = pdf.beginText(40, 170)
    text1.setFont('Helvetica', 9)
    text1.textLine(r)
    pdf.drawText(text1)
    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='Doc.pdf')

