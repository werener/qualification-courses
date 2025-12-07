# app/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from datetime import datetime
from collections import defaultdict

AVAILIABLE_COURSES = [
    "Управление проектами",
    "Цифровая трансформация",
    "Лидерство и командообразование",
    "Финансовый менеджмент",
    "Стратегическое планирование",
]
COURSES_TO_INDEXES = dict(map(lambda x: x[::-1], enumerate(AVAILIABLE_COURSES)))

COMPANY_ESTABLISHMENT_DATE = 1992


def index(request):
    # Get messages from session if they exist
    success = request.session.pop("success", False)
    database_error_message = request.session.pop("database_error_message", "")
    show_message = request.session.pop("show_message", False)

    context = {
        "courses": AVAILIABLE_COURSES,
        "indexation": COURSES_TO_INDEXES,
        "establishment": COMPANY_ESTABLISHMENT_DATE,
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
    return render(
        request,
        "report.html",
        {"courses": AVAILIABLE_COURSES, "indexation": COURSES_TO_INDEXES},
    )


REPORT_TYPES = {
    "completion_dynamics": "Динамика прохождений курсов",
    "course_popularity_month": "Популярность курсов (по месяцам)",
    "course_popularity_week": "Популярность курсов (по неделям)",
    "courses_by_position": "Популярность по должностям",
}


def visualization(request):
    print("-" * 50)

    data = dict(request.POST)

    #   courses
    chosen_courses = [course for course in AVAILIABLE_COURSES if course in data]

    #   dates
    start_date = datetime.strptime(data["start_date"][0], "%Y-%m-%d").date()
    end_date = datetime.strptime(data["end_date"][0], "%Y-%m-%d").date()
    enrollments = Enrollment.objects.filter(
        start_date__gte=start_date, end_date__lte=end_date, course__in=chosen_courses
    )

    #   types
    chart_type = data["chart_type"][0]
    report_type = data["report_type"][0]
    label = REPORT_TYPES[report_type]

    #   LOGIC
    match report_type:
        case "completion_dynamics":
            #   count each courses' attendance
            counts = defaultdict(int)
            for enrollment in enrollments:
                counts[enrollment.course] += 1

            #   create data for graph generation
            generation_data = {
                "labels": chosen_courses,
                "datasets": [
                    {
                        "label": label,
                        "data": [counts[course] for course in chosen_courses],
                        "backgroundColor": "#6b8cbc",
                    }
                ],
            }
    #     case "course_popularity_month":
    #         ...
    #     case "course_popularity_week":
    #         ...
    #     case "courses_by_position":
    #         ...

    chart_data = {
        "start_date": start_date,
        "end_date": end_date,
        "chosen_courses": chosen_courses,
        "chart_type": chart_type,
        "label": label,
        "data_input": generation_data,
    }
    
    print(chart_data)
    print("-" * 50)
    # return render(
    #     request,
    #     "report.html",
    #     {"courses": AVAILIABLE_COURSES, "indexation": COURSES_TO_INDEXES},
    # )
    print(generation_data)
    return render(
        request, "graph.html", {"courses": AVAILIABLE_COURSES, "chart_data": chart_data}
    )


"""
    bar: {
        labels: ['Январь', 'Февраль', 'Март', 'Апрель', 'Май'],
        datasets: [{
            label: 'Доход',
            data: [12000, 19000, 3000, 5000, 2000],
            backgroundColor: '#6b8cbc'
        }]
    },
    pie: {
        labels: ['Красный', 'Синий', 'Желтый'],
        datasets: [{
            data: [300, 50, 100],
            backgroundColor: [
                '#ff7e5f',
                '#4a6fa5',
                '#ffd166'
            ]
        }]
"""
