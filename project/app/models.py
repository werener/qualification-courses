from django.db import models



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
    course = models.CharField(max_length=300, verbose_name="Курс")
    start_date = models.DateField(verbose_name="Дата начала курса")
    end_date = models.DateField(verbose_name="Дата окончания курса")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата записи")
    
    class Meta:
        verbose_name = "Запись на курс"
        verbose_name_plural = "Записи на курс"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.employee} ({self.course}): {self.start_date} - {self.end_date}"
