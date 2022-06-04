from django.urls import path
from DunbartonApp import views
urlpatterns = [
    path('dunbarton/home',views.LandingPageFunction, name='LandingPageFunction')
]
