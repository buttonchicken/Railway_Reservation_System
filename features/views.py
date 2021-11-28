from django.db.models.expressions import Value
from django.db.models.fields import CharField
from django.http.request import HttpHeaders, HttpRequest
from .models import Booking,Member,Train,TrainSeat,TrainStatus
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth import authenticate,login
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
import math
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
import datetime
import random
import string
import time

#converts date to required timestamp

def getTimestampFromDate(date):
    departure_day = datetime.datetime.strptime(date[:10],"%d-%m-%Y").weekday()
    time_mins = int(date[-5:-3]) + (int(date[-8:-6])*60)
    return departure_day*1440 + time_mins 

def bookTrain(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            t_id=request.POST.get('tid')
            d_st=request.POST.get('dstation')
            a_st=request.POST.get('astation')
            d_time=request.POST.get('d_date')
            a_time=request.POST.get('a_date')
            total_cost=request.POST.get('tcost')
            num_seats=int(request.POST.get('num_seats'))
            departure_timestamp = getTimestampFromDate(d_time)
            arrival_timestamp = getTimestampFromDate(a_time)
            trains=[]
            #checking for direct train else for indirect routes
            try: 
                trains.append(Train.objects.get(train_id=t_id,departure_station=d_st,arrival_station=a_st,departure_time=departure_timestamp))
            except ObjectDoesNotExist:
                trains = Train.objects.filter(train_id=t_id,departure_time__gte=departure_timestamp,arrival_time__lte=arrival_timestamp)
            train_seats = []
            for train in trains:
                train_seat = None
                try:
                    train_departure_date=(datetime.datetime.strptime(d_time,"%d-%m-%Y, %H:%M:%S")+datetime.timedelta(minutes=(train.departure_time-departure_timestamp))).strftime("%d-%m-%Y, %H:%M:%S")
                    train_arrival_date=(datetime.datetime.strptime(d_time,"%d-%m-%Y, %H:%M:%S")+datetime.timedelta(minutes=(train.arrival_time-departure_timestamp))).strftime("%d-%m-%Y, %H:%M:%S")

                    train_seat = TrainSeat.objects.get(
                        train_id=train.train_id,
                        departure_station=train.departure_station,
                        arrival_station=train.arrival_station,
                        departure_date=train_departure_date,
                        arrival_date=train_arrival_date
                    )
                except ObjectDoesNotExist:
                    train_seat = TrainSeat()
                    train_seat.train_id=train.train_id
                    train_seat.departure_station=train.departure_station
                    train_seat.arrival_station=train.arrival_station
                    train_seat.departure_date=train_departure_date
                    train_seat.arrival_date=train_arrival_date
                    train_seat.booked_seats=""
                    train_seat.all_seats="1,2,3,4,5,6,7,8,9,10" #taking total available seats as 10 for example

                train_seats.append(train_seat)

            available_seats = None

            for train_seat in train_seats:
                booked_seats = train_seat.booked_seats.split(",")
                all_seats = train_seat.all_seats.split(",")
                tmp_available_seats = [seat for seat in all_seats if seat not in booked_seats]
                if available_seats is None:
                    available_seats=tmp_available_seats
                else:
                    #keep taking intersection of available seats as user needs to have the same seat number
                    #throughout the journey irrespective of the stops in between
                    available_seats = [value for value in available_seats if value in tmp_available_seats]

            #checking if number of seats to be booked are available
            if(num_seats<=len(available_seats)):
                seats_to_book = available_seats[:num_seats]

                for train_seat in train_seats:
                    booked_seats = train_seat.booked_seats.split(",")
                    if(booked_seats[0]==''):
                        booked_seats=[]
                    train_seat.booked_seats = ",".join(booked_seats+seats_to_book)
                    train_seat.save()
                
                #booking the seats
                b=Booking()
                
                b.booked_by=request.user
                b.train_id=t_id
                b.boarding_station=d_st
                b.arrival_station=a_st
                b.board_dt=d_time
                b.arrive_dt=a_time
                b.seats_booked=num_seats
                b.total_cost=total_cost
                b.seat_nums=",".join(seats_to_book)
                b.pnr=''.join(random.choices(string.ascii_uppercase+string.digits, k = 5))
                b.save()
                return HttpResponse('<center><h1>Booking Successful</h1></center>')

            else: 
                return HttpResponse('<center><h1>Seats not available</h1></center>')

#data class to store train information to send to frontend

class TrainData:
    train_id: str
    departure_date: str
    arrival_date: str
    departure_station: str
    arrival_station: str
    cost: str
        
def searchTrain(request):
    if request.method=='POST':
        a=request.POST.get('arrive')
        d=request.POST.get('depart')
        n=request.POST.get('numseats')
        dt=request.POST.get('departuredate')
        date_today=str(datetime.date.today()) #current date
        if dt<date_today:
            return HttpResponse('<center><h1>Cannot Book for the Past!!</h1></center>')
        booking_day_index=datetime.datetime.strptime(dt,"%Y-%m-%d").weekday()
        min_departure_time=(booking_day_index)*1440
        max_departure_time=(booking_day_index+1)*1440
        
        o=Train.objects.filter(arrival_station=a, departure_station=d, departure_time__gte=min_departure_time, departure_time__lte=max_departure_time)
        trains = []
        
        for i in o :
            tmp = TrainData()
            tmp.train_id=i.train_id
            tmp.departure_station=i.departure_station
            tmp.arrival_station=i.arrival_station
            tmp.cost=i.cost
            tmp.departure_date=(datetime.datetime.strptime(dt,"%Y-%m-%d")+datetime.timedelta(minutes=i.departure_time%1440)).strftime("%d-%m-%Y, %H:%M:%S")
            tmp.arrival_date=(datetime.datetime.strptime(dt,"%Y-%m-%d")+datetime.timedelta(minutes=i.departure_time%1440)+datetime.timedelta(minutes=(i.arrival_time-i.departure_time))).strftime("%d-%m-%Y, %H:%M:%S")

            trains.append(tmp)
        del o
        if trains: #checking for direct trains
            return render(request,'list.html',{'query':trains,'d':d,'a':a,'booking_day':booking_day_index,'num':n,'departure_date':dt})
        else: #checking for indirect trains
            departing_from_desired=list(Train.objects.filter(departure_station=d,departure_time__gte=min_departure_time, departure_time__lte=max_departure_time))
            arriving_at_desired=list(Train.objects.filter(arrival_station=a))
            
            final=[]
            
            for x in departing_from_desired:
                rt=[]
                for y in arriving_at_desired:
                    if x.train_id==y.train_id:
                        rt.append(x)
                        rt.append(y)
                        final.append(rt)
            
            for x in final:
                if x[0].departure_time>=x[1].arrival_time:
                    final.remove(x)
            if not final:
                return HttpResponse('<center><h1>No trains Available</h1></center>')

            else:
                trains = []
                for i in final:
                    tmp = TrainData()
                    tmp.train_id=i[0].train_id
                    tmp.departure_station=i[0].departure_station
                    tmp.arrival_station=i[1].arrival_station
                    tmp.departure_date=(datetime.datetime.strptime(dt,"%Y-%m-%d")+datetime.timedelta(minutes=i[0].departure_time%1440)).strftime("%d-%m-%Y, %H:%M:%S")
                    tmp.arrival_date=(datetime.datetime.strptime(dt,"%Y-%m-%d")+datetime.timedelta(minutes=i[0].departure_time%1440)+datetime.timedelta(minutes=(i[1].arrival_time-i[0].departure_time))).strftime("%d-%m-%Y, %H:%M:%S")
                    
                    all_stops = Train.objects.filter(train_id=i[0].train_id,departure_time__gte=i[0].departure_time,arrival_time__lte=i[1].arrival_time)
                    total_cost=0
                    for i in all_stops:
                        total_cost+=i.cost
                    tmp.cost=total_cost
                    trains.append(tmp)
                return render(request,'list.html',{'query':trains,'d':d,'a':a,'booking_day':booking_day_index,'num':n,'departure_date':dt})
    return render(request,'search.html')

#function to fetch users current bookings

def showBookings(request):
    if request.user.is_authenticated:
        try:
            u=request.user
            try:
                Booking.objects.get(booked_by=str(u))
                o=Booking.objects.all()
                return render(request,'pnr.html',{'query':o,})
            except MultipleObjectsReturned:
                o1=Booking.objects.all()
                return render(request,'pnr.html',{'query':o1})
        except ObjectDoesNotExist:
            return HttpResponse('<center><h1>No Bookings Found!</h1></center>')
    else:
        return HttpResponse('<center><h1>Please Login First!!</h1><br><a href="/login">login here</a>')

#function to get the trains current status, have made input for RJD1 for example

def trainStatus(request):
    if request.method=='GET':
        return render(request,'trainstatus.html')
    if request.method=='POST':
        train_id=request.POST.get('train_id')
        try:
            current_status = TrainStatus.objects.get(train_id=train_id)
            last_departure_station=current_status.last_departure_station
            last_actual_departure_date=current_status.last_departure_date
            train_schedule = Train.objects.get(train_id=train_id,departure_station=last_departure_station)
            delay = getTimestampFromDate(last_actual_departure_date)-train_schedule.departure_time
            if(delay<=0):
                return render(request,'trainstatus.html',{'status':'Train '+str(train_id)+' is on Time'})
            else:
                return render(request,'trainstatus.html',{'status':'Train '+str(train_id)+' is delayed by '+str(delay)+' mins'})
        except ObjectDoesNotExist:
            return render(request,'trainstatus.html',{'status':'Train '+str(train_id)+' does not exist'})
            
#converts minutes into weekday,time(HH:MM) format

def TimeToDay(x):
    weekday=math.floor(x/1440)
    t=x%1440
    day={
        0:'Monday',
        1:'Tuesday',
        2:'Wedneday',
        3:'Thursday',
        4:'Friday',
        5:'Saturday',
        6:'Sunday',
    }
    y='{:02d}:{:02d}'.format(*divmod(t, 60))
    a=day[weekday]+","+y
    return a

#fetches the train schedule for a train ID

def trainSchedule(request):
    if request.method=='GET':
        return render(request,'trainschedule.html')
    if request.method=='POST':
        train_id=request.POST.get('train_id')
        try:
            schedule=Train.objects.filter(train_id=train_id)
            arr=[]
            for i in schedule:
                tmp = TrainData()
                tmp.train_id=i.train_id
                tmp.departure_station=i.departure_station
                tmp.arrival_station=i.arrival_station
                departs_on=int(i.departure_time)
                departing_day=TimeToDay(departs_on)
                tmp.departure_date=departing_day
                arrives_on=int(i.arrival_time)
                arriving_day=TimeToDay(arrives_on)
                tmp.arrival_date=arriving_day
                tmp.cost=i.cost
                arr.append(tmp)

            return render(request,'trainschedule.html',{'query':arr})
        except ObjectDoesNotExist:
            return HttpResponse('<h1><center>No Such Train ID !!</center></h1>')
                    