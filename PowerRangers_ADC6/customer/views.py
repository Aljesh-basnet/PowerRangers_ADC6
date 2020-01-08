from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template,Context
from .models import Booking

def view_Booking_lists(request):
    list_of_Booking= BookRoom.objects.all()
    print(list_of_Booking)
    context_variable = {
        'booking':list_of_Booking
    }
    return render(request,'bookings/bookings.html',context_variable)
