from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template,Context
from .models import BookRoom
from django.db.models import Q
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage




def view_Booking_lists(request):
    list_of_Booking= BookRoom.objects.all()
    
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

def booking_update_forms(request, ID):

    
    book_obj = BookRoom.objects.get(id=ID)
    
    context_varible = {
        'book':book_obj
    }
    return render(request,'bookingsupdateform.html',context_varible)

def booking_update_save(request, ID):
    book_object = BookRoom.objects.get(id=ID)
    
    book_form_data = request.POST
    
    book_object.cname = request.POST['CustomerName']
    book_object.roomtype =request.POST['RoomType']
    book_object.roomno = request.POST['RoomNo']
    book_object.cemail = request.POST['CustomerEmail']
    book_object.ccontact = request.POST['CustomerContact']
    book_object.save();

    return HttpResponse("Record Updated!!")


def delete_book(request, ID):
    book_id = int(ID)
    try:
        book_sel = BookRoom.objects.get(id = ID)
    except BookRoom.DoesNotExist:
        return redirect('index')
    book_sel.delete()
    # return redirect('index')
    return HttpResponse("Record Deleted!!")

def search(request):
    return render(request, 'search.html')

def searchresults(request):
    query = request.POST['search']
    result = BookRoom.objects.filter(Q(cname__icontains=query) | Q(cemail__icontains=query) | Q(ccontact__icontains=query))
    Context = {'result': result}
    return render(request, 'searchlist.html', Context)


def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        file_object = FileSystemStorage()
        file_object.save(uploaded_file.name, uploaded_file)
    return render(request, 'uploadfile.html')