from django.contrib import admin
from django.urls import path,include
import features
from . import views
urlpatterns = [
path('admin/', admin.site.urls),
path('',include('features.urls')),
path('',views.home),
path('login',views.log),
path('register',views.register),
path('logout',views.logout)
]