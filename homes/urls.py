
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:fpack_id>', views.flight, name='flight'),
    path('book<int:flight_id>', views.book, name='book'),
    path('tour<int:tour_id>', views.tour, name='tour')
   ]
