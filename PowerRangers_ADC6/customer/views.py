from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template,Context
from .models import BookRoom



def view_Booking_lists(request):
    list_of_Booking= BookRoom.objects.all()
    print(list_of_Booking)
    context_variable = {
        'booking':list_of_Booking
    }
    return render(request,'bookings.html',context_variable)

def booking_form(request):
    return render(request,'bookingform.html')



def booking_save(request):
    if request.method== 'POST': 
        get_all =request.POST
        get_cname =request.POST['CustomerName']
        get_room_type= request.POST['RoomType']
        get_room_no =request.POST['RoomNo']
        get_cemail= request.POST['CustomerEmail']
        get_ccontact = request.POST['CustomerContact']
        Booking_obj = BookRoom(cname=get_cname,roomtype=get_room_type,roomno=get_room_no,cemail=get_cemail,ccontact=get_ccontact)
        Booking_obj.save()
        return HttpResponse("Record saved")
    else:
        return HttpResponse("Error record saving")

def booking_update_forms(request):

    print(ID)
    book_obj = BookRoom.objects.get(id=ID)
    print(book_obj)
    context_varible = {
        'book':book_obj
    }
    return render(request,'bookings/bookingupdateform.html',context_varible)

def booking_update_save(request,ID):
    book_obj = BookRoom.objects.get(id=ID)
    print(book_obj)
    book_form_data = request.POST
    print(book_form_data)
    book_obj.cname = request.POST['CustomerName']
    book_obj.roomtype =request.POST['RoomType']
    book_obj.roomno = request.POST['RoomNo']
    book_obj.cemail = request.POST['CustomerEmail']
    book_obj.ccontact = request.POST['CustomerContact']
    book_obj.save()

    return HttpResponse("Record Updated!!")