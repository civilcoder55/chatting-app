
from django.contrib import admin
from django.urls import path,include
from messenger import views
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('messenger/', include('messenger.urls')),
    path('__debug__/', include(debug_toolbar.urls)),

]

handler404 =views.home