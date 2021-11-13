from django.db import models


# Create your models here.
class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)
    country = models.CharField(max_length=64, null=True)

    def __str__(self):
        return f'{self.city} | ({self.code})'


class AddFlight(models.Model):
    date = models.DateField()
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departures')
    dtime = models.TimeField()
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrivals')
    atime = models.TimeField()

    def __str__(self):
        return f'{self.id} | {self.date} at {self.dtime} from {self.origin.city} to {self.destination.city} at {self.atime}'


class Passenger(models.Model):
    fname = models.CharField(max_length=64)
    lname = models.CharField(max_length=64)
    flights = models.ManyToManyField(AddFlight, blank=True, related_name='passengers')

    def __str__(self):
        return f'{self.fname} {self.lname}'


class Price(models.Model):
    flight = models.OneToOneField(AddFlight, blank=True, on_delete=models.CASCADE, related_name='addflight')
    saver = models.PositiveIntegerField()
    economy = models.PositiveIntegerField()
    business = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.flight} Tk{self.saver} Tk{self.economy} Tk{self.business}'


class Agent(models.Model):
    name = models.CharField(max_length=50)
    contact_person = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=24)
    address = models.CharField(max_length=100)
    starting_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Agent ID {self.id} name {self.name} contact no {self.contact_no}'


class Booked(models.Model):
    date = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=24)
    last_name = models.CharField(max_length=24)
    email = models.EmailField()
    contact_no = models.CharField(max_length=24)
    agent = models.ForeignKey(Agent, blank=True, null=True, on_delete=models.CASCADE, related_name='agent_booked')
    flight = models.ForeignKey(AddFlight, on_delete=models.CASCADE, related_name='flight_boooked')
    no_of_adult_sit = models.PositiveSmallIntegerField()
    no_of_child_sit = models.PositiveSmallIntegerField()
    sit_type = models.CharField(max_length=16)
    total_amount = models.PositiveIntegerField()
    return_flight = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return f'Flight {self.flight}, {self.no_of_adult_sit} adult and {self.no_of_child_sit} child  {self.sit_type} ' \
               f'class sit booked by {self.first_name} {self.last_name} at {self.date} contact email: {self.email} ' \
               f'contact no: {self.contact_no} total paid{self.total_amount} '
