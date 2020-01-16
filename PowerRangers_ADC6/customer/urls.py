from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns =[
    path('booking/',views.view_Booking_lists),
    path('bookingform/',views.booking_form),
    path('bookingform/save',views.booking_save),
    path('booking/update/<int:ID>',views.booking_update_forms),
    path('booking/update/update/<int:ID>',views.booking_update_save),
    path('booking/delete/<int:ID>', views.delete_book),
    path('search/',views.search),
    path('search/searchlist',views.searchresults),
    path('upload/',views.upload),
    path('signup/',views.register_user),
    path('login/',views.authenticate_user)
    
   
]