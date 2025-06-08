from django.contrib import admin
from .models import *

# The `StudentAdmin` class defines the display, search, filter, and ordering settings for the admin
# interface of a student model.
class StudentAdmin(admin.ModelAdmin):
    list_display = ('username', 'student_id', 'institution', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'student_id', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')
    ordering = ('username',)

admin.site.register(Student, StudentAdmin)
