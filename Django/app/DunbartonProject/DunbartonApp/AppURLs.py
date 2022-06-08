from django.urls import path
from DunbartonApp import views
urlpatterns = [
    path('dunbarton/Scan',views.ScanPageFunction, name='ScanPageFunction')
]
