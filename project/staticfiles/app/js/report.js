document.addEventListener('DOMContentLoaded', function() {
    // Элементы формы
    const reportForm = document.getElementById('reportForm');
    const selectAllBtn = document.getElementById('selectAll');
    const deselectAllBtn = document.getElementById('deselectAll');
    const previewBtn = document.getElementById('previewBtn');
    const resetBtn = document.getElementById('resetBtn');
    const quickDateBtns = document.querySelectorAll('.btn-quick');
    
    // Выбор всех курсов
    selectAllBtn.addEventListener('click', function() {
        
        const checkboxes = document.querySelectorAll('input[name="selected_courses"]');
        
        checkboxes.forEach(checkbox => {
            checkbox.checked = true;
        });
    });
    
    // Снятие выделения со всех курсов
    deselectAllBtn.addEventListener('click', function() {
        const checkboxes = document.querySelectorAll('input[name="selected_courses"]');
        checkboxes.forEach(checkbox => {
            checkbox.checked = false;
        });
    });
    
    // Быстрый выбор временного промежутка
    quickDateBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const days = parseInt(this.getAttribute('data-days'));
            const endDate = new Date();
            const startDate = new Date();
            startDate.setDate(endDate.getDate() - days);
            
            document.getElementById('start_date').value = formatDate(startDate);
            document.getElementById('end_date').value = formatDate(endDate);
        });
    });
    
    // Предварительный просмотр
    previewBtn.addEventListener('click', function() {
        if (validateForm()) {
            const formData = new FormData(reportForm);
            const params = new URLSearchParams(formData);
            
            // В реальном приложении здесь был бы AJAX запрос
            alert('Предварительный просмотр для:\n' + 
                  `Тип отчета: ${getReportTypeText(formData.get('report_type'))}\n` +
                  `Период: ${formData.get('start_date')} - ${formData.get('end_date')}\n` +
                  `Курсов выбрано: ${formData.getAll('selected_courses').length}`);
        }
    });
    
    // Сброс формы
    resetBtn.addEventListener('click', function() {
        if (confirm('Вы уверены, что хотите сбросить все параметры?')) {
            reportForm.reset();
            // Установка дат по умолчанию
            const today = new Date();
            const monthAgo = new Date();
            monthAgo.setMonth(today.getMonth() - 1);
            
            document.getElementById('start_date').value = formatDate(monthAgo);
            document.getElementById('end_date').value = formatDate(today);
        }
    });
    
    // Валидация формы при отправке
    reportForm.addEventListener('submit', function(e) {
        if (!validateForm()) {
            e.preventDefault();
        }
    });
    
    // Вспомогательные функции
    function formatDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }
    
    function validateForm() {
        const startDate = new Date(document.getElementById('start_date').value);
        const endDate = new Date(document.getElementById('end_date').value);
        const selectedCourses = document.querySelectorAll('input[name="selected_courses"]:checked');
        
        // Проверка дат
        if (startDate > endDate) {
            alert('Дата начала не может быть позже даты окончания');
            return false;
        }
        
        // Проверка выбора курсов
        // if (selectedCourses.length === 0) {
        //     alert('Выберите хотя бы один курс для анализа');
        //     return false;
        // }
        
        return true;
    }
    
    function getReportTypeText(type) {
        const types = {
            'general_dynamics': 'Общая динамика и загрузка',
            'course_effectiveness': 'Эффективность курсов',
            'audience_analysis': 'Анализ аудитории',
            'geographic_time': 'Географический и временной анализ',
            'planning_forecast': 'Прогнозирование и выполнение плана'
        };
        return types[type] || type;
    }
    
    // Динамическое обновление доступных типов графиков в зависимости от типа отчета
    const reportTypeRadios = document.querySelectorAll('input[name="report_type"]');
    const chartTypeSelect = document.getElementById('chart_type');
    
    reportTypeRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            updateChartTypes(this.value);
        });
    });
    
    function updateChartTypes(reportType) {
        // Очищаем текущие options
        chartTypeSelect.innerHTML = '';
        
        let chartTypes = [];
        
        switch(reportType) {
            case 'general_dynamics':
                chartTypes = [
                    {value: 'line', text: 'Линейный график'},
                    {value: 'bar', text: 'Столбчатая диаграмма'},
                    {value: 'area', text: 'Областная диаграмма'}
                ];
                break;
            case 'course_effectiveness':
                chartTypes = [
                    {value: 'bar', text: 'Столбчатая диаграмма'},
                    {value: 'pie', text: 'Круговая диаграмма'},
                    {value: 'line', text: 'Линейный график'}
                ];
                break;
            case 'audience_analysis':
                chartTypes = [
                    {value: 'pie', text: 'Круговая диаграмма'},
                    {value: 'bar', text: 'Столбчатая диаграмма'},
                    {value: 'treemap', text: 'Древовидная диаграмма'}
                ];
                break;
            case 'geographic_time':
                chartTypes = [
                    {value: 'bar', text: 'Столбчатая диаграмма'},
                    {value: 'heatmap', text: 'Тепловая карта'},
                    {value: 'line', text: 'Линейный график'}
                ];
                break;
            case 'planning_forecast':
                chartTypes = [
                    {value: 'line', text: 'Линейный график'},
                    {value: 'bar', text: 'Столбчатая диаграмма'}
                ];
                break;
            default:
                chartTypes = [
                    {value: 'line', text: 'Линейный график'},
                    {value: 'bar', text: 'Столбчатая диаграмма'}
                ];
        }
        
        // Добавляем новые options
        chartTypes.forEach(chart => {
            const option = document.createElement('option');
            option.value = chart.value;
            option.textContent = chart.text;
            chartTypeSelect.appendChild(option);
        });
    }
    
    // Инициализация при загрузке
    const initialReportType = document.querySelector('input[name="report_type"]:checked').value;
    updateChartTypes(initialReportType);
});