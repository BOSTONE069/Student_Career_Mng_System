from django.contrib import admin
from .models import ExamRegistration

# This class defines an admin interface for managing exam registrations with specified list display
# fields, search fields, filters, and ordering.
class ExamRegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'course_code', 'course_title', 'semester', 'year', 'registered_on', 'is_verified')
    search_fields = ('student__username', 'course_code', 'course_title', 'semester', 'year')
    list_filter = ('semester', 'year', 'is_verified')
    ordering = ('-registered_on',)

admin.site.register(ExamRegistration, ExamRegistrationAdmin)
