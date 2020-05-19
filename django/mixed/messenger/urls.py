from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home , name='messengerHome'),
    path('<int:id>/', views.private , name='private'),
]