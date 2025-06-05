from django.contrib import admin
from .models import Institution, Program, Course, Unit, Fee

# Register your models here.

# The `InstitutionAdmin` class defines a Django admin model with fields for name, code, and website.
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'website')

# The `ProgramAdmin` class defines a Django admin model with fields for institution, name, and
# duration in years.
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('institution', 'name', 'duration_years')

# The `CourseAdmin` class defines a Django admin model with specified fields for display in the admin
# interface.
class CourseAdmin(admin.ModelAdmin):
    list_display = ('program', 'title', 'semester')

# The `UnitAdmin` class in Python defines a Django admin model with specified fields for display in
# the admin interface.
class UnitAdmin(admin.ModelAdmin):
    list_display = ('course', 'code', 'name')

# The `FeeAdmin` class defines the display fields for a fee administration panel in a Python Django
# project.
class FeeAdmin(admin.ModelAdmin):
    list_display = ('program', 'fee_type', 'amount', 'currency')

admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Fee, FeeAdmin)
