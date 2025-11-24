from django.contrib import admin
from .models import  Employee, Enrollment


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'middle_name', 'position', 'email']
    search_fields = ['last_name', 'first_name', 'middle_name', 'position']
    list_filter = ['position']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['employee', 'course', 'start_date', 'end_date']
    list_filter = ['course', 'start_date', 'end_date']
    search_fields = ['employee__last_name', 'employee__first_name', 'course__name']
    date_hierarchy = 'start_date'

    