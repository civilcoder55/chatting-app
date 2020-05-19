
from django.contrib import admin
from django.urls import path,include
from messenger import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('messenger/', include('messenger.urls')),

]
handler404 =views.home