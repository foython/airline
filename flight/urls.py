
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_flight, name='flights_list'),
    path('<int:flight_id>', views.flight, name='flights'),
    path('search', views.search, name='search'),
    path('book/', views.returnbook, name='rbook'),
    path('booked', views.con_booked, name='booked'),
    path('confirm', views.confirm, name='confirm'),
    path('print', views.print, name='print')
   ]
