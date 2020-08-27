from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Student

admin.site.register(Student)
admin.site.unregister(Group)
