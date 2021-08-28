from django.urls import path
from . import views

urlpatterns = [
    path('', views.home , name='messengerHome'),
    path('<int:id>/history', views.history , name='history'),
    path('<int:id>/', views.PrivateView.as_view() , name='private'),
]