from django.db import models

# Create your models here.
class Member(models.Model): #class for users
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=20)
    email=models.CharField(max_length=100)
    number=models.CharField(max_length=10)

class TrainSeat(models.Model): #class to help with seat matrix
    train_id=models.CharField(max_length=6)
    departure_station=models.CharField(max_length=1)
    arrival_station=models.CharField(max_length=1)
    departure_date=models.CharField(max_length=100)
    arrival_date=models.CharField(max_length=100)
    booked_seats=models.CharField(max_length=1000)
    all_seats=models.CharField(max_length=1000)

class Train(models.Model): #standard class for any train
    train_id=models.CharField(max_length=6)
    departure_station=models.CharField(max_length=1)
    arrival_station=models.CharField(max_length=1)
    departure_time=models.BigIntegerField()
    arrival_time=models.BigIntegerField()
    cost=models.IntegerField()

class Booking(models.Model): #class to handle bookings
    booked_by=models.CharField(max_length=100)
    train_id=models.CharField(max_length=6)
    boarding_station=models.CharField(max_length=1)
    arrival_station=models.CharField(max_length=1)
    board_dt=models.CharField(max_length=25,default='')
    arrive_dt=models.CharField(max_length=25,default='')
    seats_booked=models.IntegerField()
    total_cost=models.BigIntegerField()
    seat_nums=models.CharField(max_length=100,default='')
    pnr=models.CharField(max_length=106)

class TrainStatus(models.Model): #class to update train staus
    train_id=models.CharField(max_length=6)
    last_departure_station=models.CharField(max_length=1)
    last_departure_date=models.CharField(max_length=100)


def __str__(self):
        return self.username