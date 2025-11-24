from django.contrib import admin
from .models import Role, Course, Employee, Enrollment, Statistics

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'middle_name', 'position', 'email']
    search_fields = ['last_name', 'first_name', 'middle_name', 'position']
    list_filter = ['position']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['employee', 'course', 'start_date', 'end_date', 'completion_id']
    list_filter = ['course', 'start_date', 'end_date']
    search_fields = ['employee__last_name', 'employee__first_name', 'course__name']
    date_hierarchy = 'start_date'

@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    list_display = ['course', 'month_year', 'participants_count', 'average_participants']
    list_filter = ['course', 'month_year']
    readonly_fields = ['calculated_at']