# courses/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('submit/', views.submit_data, name='submit_data'),
    path('report/', views.get_report_page),
    path('visualization/', views.visualization, name='visualization'),
]