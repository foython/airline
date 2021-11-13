from django.contrib import admin
from .models import Airport, AddFlight, Passenger, Price, Agent, Booked

# Register your models here.
admin.site.register(Airport)
admin.site.register(AddFlight)
admin.site.register(Passenger)
admin.site.register(Price)
admin.site.register(Agent)
admin.site.register(Booked)
