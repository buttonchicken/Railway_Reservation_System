from django.contrib import admin
from django.urls import path,include
from features import views
urlpatterns = [
    path('searchTrain',views.searchTrain),
    path('book',views.bookTrain),
    path('showBookings',views.showBookings),
    path('trainStatus',views.trainStatus),
    path('trainSchedule',views.trainSchedule)
]