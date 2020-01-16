from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template,Context
from .models import BookRoom
from django.db.models import Q
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages




def view_Booking_lists(request):
    list_of_Booking= BookRoom.objects.all()
    
    context_variable = {
        'booking':list_of_Booking
    }
    return render(request,'Bookings/bookings.html',context_variable)

def booking_form(request):
    return render(request,'Bookings/bookingform.html')



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
    return render(request,'Bookings/bookingsupdateform.html',context_varible)

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
    return render(request, 'Bookings/search.html')

def searchresults(request):
    query = request.POST['search']
    result = BookRoom.objects.filter(Q(cname__icontains=query) | Q(cemail__icontains=query) | Q(ccontact__icontains=query))
    Context = {'result': result}
    return render(request, 'Bookings/searchlist.html', Context)


def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        file_object = FileSystemStorage()
        file_object.save(uploaded_file.name, uploaded_file)
    return render(request, 'Bookings/uploadfile.html')


def register_user(request):
    if request.method =="GET":
        return render(request,'Registration/register.html')

    elif request.method=="POST":
    
        Username=request.POST['input_username']
        Password1=request.POST['input_password1']
        Password2=request.POST['input_password2']
        Email=request.POST['input_email']


        if Password1==Password2:
            if User.objects.filter(username=Username).exists():
                messages.info(request,'Username exists!!!')
                return render(request,'Registration/register.html')

            elif User.objects.filter(email=Email).exists():
                messages.info(request,'Email exists!!!')
                return render(request,'Registration/register.html')

            else:
                user_obj = User.objects.create_user(username=Username,password=Password1,email=Email)
                user_obj.save()
                return HttpResponse("Signup Successful")
        else: 
            messages.info(request,'Password do not match!!!')
            return render(request,'Registration/register.html')

        

def authenticate_user(request):
    if request.method == "GET":
        return render(request,'Registration/login.html')
    
    else: 
        user= authenticate(username=request.POST['input_username'],password=request.POST['input_password'])
        if user is not None:
            login(request,user)
            return render(request,'Bookings/bookingform.html')
        else:
            messages.info(request,'invalid username or password')
            return render(request,'Registration/login.html')
