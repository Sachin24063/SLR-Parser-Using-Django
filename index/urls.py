from django.contrib import admin
from django.urls import path
from .views import index , check_string

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , index , name = "index"),
    path('check_string' , check_string , name = "check_string")
]

