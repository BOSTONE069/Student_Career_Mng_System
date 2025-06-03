from django.contrib import admin
from .models import Institution, Program, Course, Unit, Fee

# Register your models here.

class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'website')

class ProgramAdmin(admin.ModelAdmin):
    list_display = ('institution', 'name', 'duration_years')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('program', 'title', 'semester')

class UnitAdmin(admin.ModelAdmin):
    list_display = ('course', 'code', 'name')

class FeeAdmin(admin.ModelAdmin):
    list_display = ('program', 'fee_type', 'amount', 'currency')

admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Fee, FeeAdmin)
