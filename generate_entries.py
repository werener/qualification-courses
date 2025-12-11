import requests
from datetime import datetime, timedelta
import random
import string

# URL вашего приложения
BASE_URL = "http://localhost:8000"  # Измените на ваш URL

# Доступные курсы
AVAILABLE_COURSES = [
    "Управление проектами",
    "Цифровая трансформация",
    "Лидерство и командообразование",
    "Финансовый менеджмент",
    "Стратегическое планирование",
]

# Базы данных имен для генерации
LAST_NAMES = ["Иванов", "Петров", "Сидоров", "Кузнецов", "Попов", "Васильев", 
              "Смирнов", "Новиков", "Фёдоров", "Морозов", "Волков", "Алексеев",
              "Лебедев", "Семенов", "Егоров", "Павлов", "Козлов", "Степанов",
              "Николаев", "Орлов", "Андреев", "Макаров", "Никитин", "Захаров"]

FIRST_NAMES = ["Александр", "Алексей", "Андрей", "Антон", "Артём", "Борис",
               "Вадим", "Валентин", "Валерий", "Виктор", "Виталий", "Владимир",
               "Владислав", "Геннадий", "Георгий", "Григорий", "Даниил", "Денис",
               "Дмитрий", "Евгений", "Иван", "Игорь", "Кирилл", "Константин"]

MIDDLE_NAMES = ["Александрович", "Алексеевич", "Анатольевич", "Андреевич",
                "Антонович", "Аркадьевич", "Артёмович", "Борисович", "Вадимович",
                "Валентинович", "Валерьевич", "Васильевич", "Викторович",
                "Витальевич", "Владимирович", "Владиславович", "Геннадьевич",
                "Георгиевич", "Григорьевич", "Даниилович", "Денисович",
                "Дмитриевич", "Евгеньевич", "Иванович", "Игоревич"]

POSITIONS = ["Менеджер проектов", "Разработчик", "Аналитик", "Дизайнер",
             "Тестировщик", "Архитектор", "Руководитель отдела", "Специалист",
             "Консультант", "Инженер", "Эксперт", "Координатор", "Администратор",
             "Руководитель направления", "Ведущий специалист", "Младший специалист"]

# Функция из первого варианта
# utils.py
import requests
from datetime import datetime, timedelta
import random
import string

# URL вашего приложения
BASE_URL = "http://localhost:8000"  # Измените на ваш URL

# Сохраняем CSRF-токен между запросами
CSRF_TOKEN = None
SESSION_COOKIES = None

def get_csrf_token():
    """
    Получает CSRF-токен и cookies с главной страницы
    """
    global CSRF_TOKEN, SESSION_COOKIES
    
    try:
        # Получаем главную страницу для получения CSRF-токена
        response = requests.get(f"{BASE_URL}/")
        response.raise_for_status()
        
        # Ищем CSRF-токен в cookies
        if 'csrftoken' in response.cookies:
            CSRF_TOKEN = response.cookies['csrftoken']
        elif 'csrf' in response.cookies:
            CSRF_TOKEN = response.cookies['csrf']
        
        # Сохраняем cookies сессии
        SESSION_COOKIES = response.cookies
        
        # Если не нашли в cookies, пробуем найти в HTML
        if not CSRF_TOKEN:
            import re
            csrf_match = re.search(r'name=["\']csrfmiddlewaretoken["\'] value=["\']([^"\']+)["\']', response.text)
            if csrf_match:
                CSRF_TOKEN = csrf_match.group(1)
        
        return CSRF_TOKEN is not None
        
    except Exception as e:
        print(f"Ошибка при получении CSRF-токена: {e}")
        return False

def create_enrollment_via_endpoint(enrollment_data, base_url=BASE_URL):
    """
    Создает запись Enrollment через эндпоинт /submit/
    с поддержкой CSRF-токена
    """
    global CSRF_TOKEN, SESSION_COOKIES
    
    endpoint = f"{base_url}/submit/"
    
    # Пытаемся получить CSRF-токен, если его еще нет
    if not CSRF_TOKEN:
        if not get_csrf_token():
            return {
                "success": False,
                "error": "Не удалось получить CSRF-токен",
                "status_code": None,
                "data": enrollment_data
            }
    
    # Подготавливаем заголовки с CSRF-токеном
    headers = {
        'Referer': f"{base_url}/",
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': CSRF_TOKEN,
    }
    
    try:
        # Отправляем POST-запрос с CSRF-токеном и cookies
        response = requests.post(
            endpoint, 
            data=enrollment_data,
            headers=headers,
            cookies=SESSION_COOKIES
        )
        
        response.raise_for_status()
        
        # Обновляем cookies из ответа
        if response.cookies:
            SESSION_COOKIES.update(response.cookies)
        
        return {
            "success": True,
            "status_code": response.status_code,
            "message": "Запись успешно создана",
            "response_text": response.text[:200]  # Первые 200 символов ответа для отладки
        }
        
    except requests.exceptions.HTTPError as e:
        # Если получили 403, пробуем обновить CSRF-токен и повторить
        if e.response.status_code == 403:
            print("Получен 403, обновляем CSRF-токен...")
            get_csrf_token()  # Обновляем токен
            
            # Повторяем запрос с обновленным токеном
            try:
                response = requests.post(
                    endpoint,
                    data=enrollment_data,
                    headers={'X-CSRFToken': CSRF_TOKEN},
                    cookies=SESSION_COOKIES
                )
                response.raise_for_status()
                
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "message": "Запись успешно создана после обновления CSRF",
                    "response_text": response.text[:200]
                }
                
            except requests.exceptions.RequestException as retry_error:
                return {
                    "success": False,
                    "error": f"Повторная попытка: {str(retry_error)}",
                    "status_code": getattr(retry_error.response, 'status_code', None),
                    "data": enrollment_data
                }
        
        return {
            "success": False,
            "error": str(e),
            "status_code": e.response.status_code,
            "data": enrollment_data
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
            "status_code": getattr(e.response, 'status_code', None),
            "data": enrollment_data
        }

# Альтернативный вариант: используем Django test Client (если скрипт запускается в Django-окружении)
def create_enrollment_with_django_client(enrollment_data):
    """
    Альтернативный вариант для использования внутри Django-проекта
    """
    try:
        from django.test import Client
        from django.urls import reverse
        
        client = Client()
        
        # Получаем CSRF-токен через GET-запрос
        response = client.get('/')
        csrf_token = client.cookies['csrftoken'].value
        
        # Отправляем POST-запрос с CSRF-токеном
        response = client.post(
            reverse('submit_data'),  # или '/submit/'
            data=enrollment_data,
            HTTP_X_CSRFTOKEN=csrf_token
        )
        
        if response.status_code == 200:
            return {
                "success": True,
                "status_code": response.status_code,
                "message": "Запись успешно создана"
            }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}",
                "status_code": response.status_code,
                "data": enrollment_data
            }
            
    except ImportError:
        return {
            "success": False,
            "error": "Django не установлен или скрипт запущен вне Django-окружения",
            "status_code": None,
            "data": enrollment_data
        }

# Дополнительная функция для отладки
def test_csrf_connection():
    """Тестирует соединение и получение CSRF-токена"""
    print("Тестирование соединения с сервером...")
    print(f"URL: {BASE_URL}")
    
    try:
        # Пробуем получить главную страницу
        response = requests.get(f"{BASE_URL}/")
        print(f"Статус GET /: {response.status_code}")
        
        # Пробуем получить CSRF-токен
        if get_csrf_token():
            print(f"CSRF-токен получен: {CSRF_TOKEN[:20]}...")
            print("Cookies сессии получены")
            
            # Тестовый POST-запрос
            test_data = {
                "lastName": "Тестовый",
                "firstName": "Сотрудник",
                "middleName": "Тестович",
                "position": "Тестировщик",
                "email": "test@example.com",
                "course": "Управление проектами",
                "startDate": "2024-01-15",
                "endDate": "2024-02-15"
            }
            
            result = create_enrollment_via_endpoint(test_data)
            print(f"Тестовый запрос: {result}")
            
        else:
            print("Не удалось получить CSRF-токен")
            
    except requests.exceptions.ConnectionError:
        print(f"Ошибка подключения к {BASE_URL}. Убедитесь, что сервер запущен.")
    except Exception as e:
        print(f"Ошибка: {e}")
        
        
def generate_random_date(start_date, end_date):
    """Генерирует случайную дату между start_date и end_date"""
    time_between = end_date - start_date
    days_between = time_between.days
    random_days = random.randrange(days_between)
    random_date = start_date + timedelta(days=random_days)
    return random_date

def generate_random_email(first_name, last_name):
    """Генерирует случайный email"""
    domains = ["gmail.com", "yandex.ru", "mail.ru", "company.com", "corp.org"]
    domain = random.choice(domains)
    
    # Разные форматы email для разнообразия
    formats = [
        f"{first_name.lower()}.{last_name.lower()}@{domain}",
        f"{first_name[0].lower()}{last_name.lower()}@{domain}",
        f"{last_name.lower()}.{first_name.lower()}@{domain}",
        f"{first_name.lower()}_{last_name.lower()}@{domain}"
    ]
    
    return random.choice(formats)

def generate_enrollment_data(employee_id, fill_all=False, fill_only_required=False):
    """
    Генерирует данные для записи на курс
    
    Args:
        employee_id: Уникальный идентификатор сотрудника
        fill_all: Заполнить все поля (включая необязательные)
        fill_only_required: Заполнить только обязательные поля
    """
    # Выбираем случайные имена
    last_name = random.choice(LAST_NAMES)
    first_name = random.choice(FIRST_NAMES)
    
    # Генерируем даты курса (от 1 до 3 месяцев)
    start_date_obj = generate_random_date(
        datetime(2024, 1, 1).date(),
        datetime(2025, 11, 1).date()  # Чтобы уложиться в срок окончания
    )
    
    # Продолжительность курса от 2 недель до 3 месяцев
    duration_days = random.randint(14, 90)
    end_date_obj = start_date_obj + timedelta(days=duration_days)
    
    # Базовые данные (обязательные + курс)
    data = {
        "lastName": f"{last_name}",  # Добавляем ID для уникальности
        "firstName": first_name,
        "middleName": "",  # По умолчанию пустое
        "position": "",  # По умолчанию пустое
        "email": "",  # По умолчанию пустое
        "course": random.choice(AVAILABLE_COURSES),
        "startDate": start_date_obj.strftime("%Y-%m-%d"),
        "endDate": end_date_obj.strftime("%Y-%m-%d"),
    }
    
    # Заполняем данные в зависимости от типа
    if fill_all:
        # 10% - заполняем ВСЕ поля
        data["middleName"] = random.choice(MIDDLE_NAMES)
        data["position"] = random.choice(POSITIONS)
        data["email"] = generate_random_email(first_name, last_name)
        
    elif fill_only_required:
        # 25% - только обязательные (поля уже заполнены по умолчанию)
        pass
        
    else:
        # 65% - частично заполняем необязательные поля
        # Случайно выбираем, какие поля заполнить
        if random.random() < 0.8:  # 80% шанс заполнить отчество
            data["middleName"] = random.choice(MIDDLE_NAMES)
        
        if random.random() < 0.7:  # 70% шанс заполнить должность
            data["position"] = random.choice(POSITIONS)
        
        if random.random() < 0.6:  # 60% шанс заполнить email
            data["email"] = generate_random_email(first_name, last_name)
    
    return data

def generate_and_send_enrollments():
    """Генерирует и отправляет 100 записей Enrollment"""
    total_records = 100
    results = {
        "success": 0,
        "failed": 0,
        "errors": []
    }
    
    # Уникальные сотрудники: 75% от 100 = 75 уникальных
    unique_employees = 75
    repeating_employees = 25
    
    # Создаем список сотрудников
    employee_ids = list(range(unique_employees))
    
    # Добавляем повторяющихся сотрудников (случайные из уникальных)
    for _ in range(repeating_employees):
        employee_ids.append(random.choice(range(unique_employees)))
    
    # Перемешиваем порядок
    random.shuffle(employee_ids)
    
    print(f"Начинаем генерацию {total_records} записей...")
    print(f"Уникальных сотрудников: {unique_employees}")
    print(f"Повторяющихся сотрудников: {repeating_employees}")
    print("-" * 50)
    
    for i, employee_id in enumerate(employee_ids):
        # Определяем тип заполнения
        if i < 10:  # 10% - заполнить все (первые 10 записей)
            fill_all = True
            fill_only_required = False
            record_type = "Все поля заполнены"
        elif i < 75:  # 65% - частично заполнить (следующие 65 записей)
            fill_all = False
            fill_only_required = False
            record_type = "Частично заполнены"
        else:  # 25% - только обязательные (последние 25 записей)
            fill_all = False
            fill_only_required = True
            record_type = "Только обязательные"
        
        # Генерируем данные
        enrollment_data = generate_enrollment_data(
            employee_id, 
            fill_all=fill_all,
            fill_only_required=fill_only_required
        )
        
        # Отправляем запрос
        print(f"Запись {i+1:3d}/100: Отправляем данные для сотрудника ID {employee_id} ({record_type})...")
        
        result = create_enrollment_via_endpoint(enrollment_data)
        
        if result["success"]:
            results["success"] += 1
            print(f"  ✓ Успешно создана")
        else:
            results["failed"] += 1
            results["errors"].append({
                "record_number": i + 1,
                "error": result.get("error", "Неизвестная ошибка"),
                "data": enrollment_data
            })
            print(f"  ✗ Ошибка: {result.get('error', 'Неизвестная ошибка')}")
    
    # Выводим статистику
    print("\n" + "=" * 50)
    print("СТАТИСТИКА ГЕНЕРАЦИИ:")
    print("=" * 50)
    print(f"Всего записей: {total_records}")
    print(f"Успешно: {results['success']}")
    print(f"Неудачно: {results['failed']}")
    
    if results['errors']:
        print("\nОшибки:")
        for error in results['errors'][:5]:  # Показываем первые 5 ошибок
            print(f"  Запись #{error['record_number']}: {error['error']}")
        if len(results['errors']) > 5:
            print(f"  ... и еще {len(results['errors']) - 5} ошибок")
    
    return results

def main():
    """Основная функция"""
    print("ГЕНЕРАТОР ТЕСТОВЫХ ДАННЫХ ДЛЯ ENROLLMENT")
    print("=" * 60)
    print("Параметры генерации:")
    print("- 100 записей Enrollment")
    print("- 75 уникальных сотрудников (75%)")
    print("- 25 повторяющихся записей (25%)")
    print("- 10 записей со всеми заполненными полями (10%)")
    print("- 65 записей с частично заполненными полями (65%)")
    print("- 25 записей только с обязательными полями (25%)")
    print(f"- Доступные курсы: {', '.join(AVAILABLE_COURSES)}")
    print("- Период: с 01.01.2024 по 01.12.2025")
    print("=" * 60)
    
    # Запрашиваем подтверждение
    response = input("\nНачать генерацию? (y/n): ").lower()
    
    if response == 'y':
        try:
            results = generate_and_send_enrollments()
            
            # Сохраняем статистику в файл
            with open('generation_report.txt', 'w', encoding='utf-8') as f:
                f.write(f"Отчет о генерации тестовых данных\n")
                f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Всего записей: {100}\n")
                f.write(f"Успешно: {results['success']}\n")
                f.write(f"Неудачно: {results['failed']}\n")
                f.write(f"\nРаспределение:\n")
                f.write(f"- Все поля заполнены: 10 записей\n")
                f.write(f"- Частично заполнены: 65 записей\n")
                f.write(f"- Только обязательные: 25 записей\n")
                
                if results['errors']:
                    f.write(f"\nОшибки:\n")
                    for error in results['errors']:
                        f.write(f"Запись #{error['record_number']}:\n")
                        f.write(f"  Ошибка: {error['error']}\n")
                        f.write(f"  Данные: {error['data']}\n\n")
            
            print(f"\nОтчет сохранен в файл: generation_report.txt")
            
        except KeyboardInterrupt:
            print("\n\nГенерация прервана пользователем")
        except Exception as e:
            print(f"\nПроизошла ошибка: {str(e)}")
    else:
        print("Генерация отменена")

# Функция для быстрого тестирования
def test_single_enrollment():
    """Тестовая функция для проверки одного Enrollment"""
    print("Тестовая отправка одной записи...")
    
    test_data = {
        "lastName": "Тестовый",
        "firstName": "Сотрудник",
        "middleName": "Тестович",
        "position": "Тестировщик",
        "email": "test@example.com",
        "course": "Управление проектами",
        "startDate": "2024-01-15",
        "endDate": "2024-02-15"
    }
    
    result = create_enrollment_via_endpoint(test_data)
    print(f"Результат: {result}")

if __name__ == "__main__":
    # Раскомментируйте нужную функцию:
    
    # Для тестирования одного запроса:
    # test_single_enrollment()
    
    # Для полной генерации 100 записей:
    main()