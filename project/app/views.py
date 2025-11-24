# app/views.py
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def submit_data(request):
    if request.method == 'POST':
        print("Данные получены:", request.POST)
        return render(request, 'index.html', {'success': True})
    return render(request, 'index.html')