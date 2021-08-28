from django.contrib import admin
from django.urls import path,re_path
from . import views

urlpatterns = [
    path('login/', views.log_in , name='login'),
    path('logout/',views.log_out,name='logout'),
    path('register/',views.registe_r,name='register'),
    path('update/',views.update,name='update'),
    re_path(r'^media/(?P<path>.*)$', views.media),
]