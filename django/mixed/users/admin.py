from django.contrib import admin
from users.models import profile_pic
from django.contrib.auth.models import Group
# Register your models here.
admin.site.unregister(Group)
admin.site.register(profile_pic)