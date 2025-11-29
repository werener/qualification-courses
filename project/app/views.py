# app/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *

AVAILIABLE_COURSES = [
    "Управление проектами",
    "Цифровая трансформация",
    "Лидерство и командообразование",
    "Финансовый менеджмент",
    "Стратегическое планирование",
]


def index(request):
    # Get messages from session if they exist
    success = request.session.pop("success", False)
    database_error_message = request.session.pop("database_error_message", "")
    show_message = request.session.pop("show_message", False)

    context = {
        "courses": AVAILIABLE_COURSES,
        "database_error_message": database_error_message,
        "success": success,
        "show_message": show_message,
    }

    return render(request, "index.html", context)


def submit_data(request):
    success = False
    database_error_message = ""
    if request.method == "POST":
        #   extract data from post request
        data = request.POST.dict()
        keys = [
            "lastName",
            "firstName",
            "middleName",
            "position",
            "email",
            "course",
            "startDate",
            "endDate",
        ]
        surname, name, midname, position, email, course, startDate, endDate = [
            data[k] for k in keys
        ]

        #   create employee if one doesn't exist already
        employee, _ = Employee.objects.get_or_create(
            last_name=surname,
            first_name=name,
            middle_name=midname,
            position=position,
            email=email,
        )

        #   handle enrollment already existing for this person
        if not Enrollment.objects.filter(employee=employee, course=course):
            enrollment, created = Enrollment.objects.get_or_create(
                employee=employee,
                course=course,
                start_date=startDate,
                end_date=endDate,
            )
            success = True
        else:
            database_error_message = "Cотрудник уже записан на этот курс"

        request.session["success"] = success
        request.session["database_error_message"] = database_error_message

    return redirect("index")


def get_report_page(request):
    return render(request, "report.html", {"courses": AVAILIABLE_COURSES})


def visualization(request):
    print(dict(request.POST))
    return render(request, "graph.html", {"courses": AVAILIABLE_COURSES})
