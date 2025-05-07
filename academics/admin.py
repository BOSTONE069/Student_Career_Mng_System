from django.contrib import admin
from .models import Institution, Program, Course, Unit

# Register your models here.

class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'website')

class ProgramAdmin(admin.ModelAdmin):
    list_display = ('institution', 'name', 'duration_years')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('program', 'title', 'semester')

class UnitAdmin(admin.ModelAdmin):
    list_display = ('course', 'code', 'name')

admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Unit, UnitAdmin)
