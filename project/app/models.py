from django.db import models

class Role(models.Model):
    """Модель для должностей сотрудников"""
    name = models.CharField(max_length=200, verbose_name="Название должности")
    
    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"
    
    def __str__(self):
        return self.name

class Course(models.Model):
    """Модель для курсов повышения квалификации"""
    name = models.CharField(max_length=300, verbose_name="Название курса")
    description = models.TextField(blank=True, verbose_name="Описание курса")
    is_active = models.BooleanField(default=True, verbose_name="Активный курс")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
    
    def __str__(self):
        return self.name

class Employee(models.Model):
    """Модель для сотрудников"""
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    middle_name = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    position = models.CharField(max_length=200, blank=True, verbose_name="Должность")
    email = models.EmailField(blank=True, verbose_name="Email")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
    
    @property
    def full_name(self):
        """Возвращает полное ФИО сотрудника"""
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"
    
    def __str__(self):
        return self.full_name

class Enrollment(models.Model):
    """Модель для записей о прохождении курсов"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Сотрудник")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    start_date = models.DateField(verbose_name="Дата начала курса")
    end_date = models.DateField(verbose_name="Дата окончания курса")
    completion_id = models.CharField(max_length=50, unique=True, verbose_name="ID прохождения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата записи")
    
    class Meta:
        verbose_name = "Запись о прохождении курса"
        verbose_name_plural = "Записи о прохождении курсов"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.employee} - {self.course}"

class Statistics(models.Model):
    """Модель для статистических данных"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    month_year = models.DateField(verbose_name="Месяц и год")
    participants_count = models.IntegerField(default=0, verbose_name="Количество участников")
    average_participants = models.FloatField(default=0, verbose_name="Среднее количество участников")
    calculated_at = models.DateTimeField(auto_now=True, verbose_name="Время расчета")
    
    class Meta:
        verbose_name = "Статистика"
        verbose_name_plural = "Статистика"
        unique_together = ['course', 'month_year']
    
    def __str__(self):
        return f"{self.course} - {self.month_year.strftime('%m.%Y')}"