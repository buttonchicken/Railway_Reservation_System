from django.contrib import admin
from .models import Member
from features.models import Train,Booking,TrainSeat,TrainStatus
# Register your models here.
admin.site.register(Member)
admin.site.register(Train)
admin.site.register(Booking)
admin.site.register(TrainSeat)
admin.site.register(TrainStatus)