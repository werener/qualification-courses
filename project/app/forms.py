from django import forms
from .models import Employee, Enrollment, Course

class EmployeeEnrollmentForm(forms.ModelForm):
    """Форма для записи сотрудника на курс"""
    course = forms.ModelChoiceField(
        queryset=Course.objects.filter(is_active=True),
        label="Курс повышения квалификации",
        empty_label="Выберите курс"
    )
    
    class Meta:
        model = Employee
        fields = ['last_name', 'first_name', 'middle_name', 'position', 'email']
        labels = {
            'last_name': 'Фамилия',
            'first_name': 'Имя', 
            'middle_name': 'Отчество',
            'position': 'Должность',
            'email': 'Email сотрудника'
        }
        widgets = {
            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Имя'}),
            'middle_name': forms.TextInput(attrs={'placeholder': 'Отчество'}),
            'position': forms.TextInput(attrs={'placeholder': 'Должность'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email@example.com'}),
        }

class EnrollmentDatesForm(forms.Form):
    """Форма для дат прохождения курса"""
    start_date = forms.DateField(
        label="Дата начала курса",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    end_date = forms.DateField(
        label="Дата окончания курса", 
        widget=forms.DateInput(attrs={'type': 'date'})
    )