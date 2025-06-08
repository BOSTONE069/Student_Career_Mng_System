from django.contrib import admin
from .models import CareerAssessment, CareerRecommendation

# This class defines the admin interface for managing career assessment data with specified list
# display fields, search fields, and ordering.
class CareerAssessmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'interests', 'skills', 'academic_strengths', 'created_at')
    search_fields = ('student__username', 'interests', 'skills', 'academic_strengths')
    ordering = ('-created_at',)

# This class defines the admin interface for managing career recommendations, displaying student,
# recommendation text, and creation date fields.
class CareerRecommendationAdmin(admin.ModelAdmin):
    list_display = ('student', 'recommendation_text', 'created_at')
    search_fields = ('student__username', 'recommendation_text')
    ordering = ('-created_at',)

admin.site.register(CareerAssessment, CareerAssessmentAdmin)
admin.site.register(CareerRecommendation, CareerRecommendationAdmin)
