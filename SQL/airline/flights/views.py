from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Flight, Passenger
from django.urls import reverse
# Create your views here.

def index(request):
    return render(request, 'flights/index.html', {
        'flights': Flight.objects.all()
    })

def flight(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    return render(request, 'flights/flight.html',{
        'flight': flight,
        'passengers': flight.passengers.all(),
        'nonpassengers': Passenger.objects.exclude(flights=flight).all()
    })

def book(request, flight_id):
    if request.method == 'POST':
        flight = Flight.objects.get(id=flight_id)
        passenger = Passenger.objects.get(id=int(request.POST['passenger']))
        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse('flight', args=(flight.id,)))