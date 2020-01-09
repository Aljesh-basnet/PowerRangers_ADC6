from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns =[
    path('booking/',views.view_Booking_lists),
    path('bookingform/',views.booking_form),
    path('bookingform/save',views.booking_save),
    path('booking/edit/<int:ID>',views.booking_update_forms),
    path('booking/update/<int:ID>',views.booking_update_save),
    path('booking/delete/<int:ID>', views.delete_book)
   
]