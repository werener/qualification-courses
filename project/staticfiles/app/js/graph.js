// Инициализация графика
let myChart = null;

// Пример данных по умолчанию
const defaultData = {
    line: {
        labels: ['Январь', 'Февраль', 'Март', 'Апрель', 'Май'],
        datasets: [{
            label: 'Продажи',
            data: [12, 19, 3, 5, 2],
            borderColor: '#4a6fa5',
            backgroundColor: 'rgba(74, 111, 165, 0.1)',
            tension: 0.1
        }]
    },
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
    },
    scatter: {
        datasets: [{
            label: 'Точечные данные',
            data: [
                {x: 10, y: 20},
                {x: 15, y: 10},
                {x: 12, y: 15},
                {x: 18, y: 5},
                {x: 5, y: 25}
            ],
            backgroundColor: '#4a6fa5'
        }]
    }
};

// DOM элементы
const chartTypeSelect = document.getElementById('chartType');
const titleInput = document.getElementById('title');
const dataInput = document.getElementById('dataInput');
const generateBtn = document.getElementById('generateBtn');
const exportBtn = document.getElementById('exportBtn');
const chartCanvas = document.getElementById('myChart');

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Установка данных по умолчанию
    updateDefaultData();
    
    // Генерация начального графика
    generateChart();
    
    // Обработчики событий
    chartTypeSelect.addEventListener('change', updateDefaultData);
    generateBtn.addEventListener('click', generateChart);
    exportBtn.addEventListener('click', exportToPDF);
});

// Обновление данных по умолчанию при смене типа графика
function updateDefaultData() {
    const type = chartTypeSelect.value;
    dataInput.value = JSON.stringify(defaultData[type], null, 2);
    
    // Установка заголовка по умолчанию
    const titles = {
        line: 'Линейный график продаж',
        bar: 'Столбчатая диаграмма доходов',
        pie: 'Круговая диаграмма распределения',
        scatter: 'Точечная диаграмма данных'
    };
    titleInput.value = titles[type];
}

// Генерация графика
function generateChart() {
    const type = chartTypeSelect.value;
    const title = titleInput.value;
    
    let data;
    try {
        data = JSON.parse(dataInput.value);
    } catch (e) {
        alert('Ошибка в формате JSON данных. Проверьте синтаксис.');
        console.error(e);
        return;
    }
    
    // Уничтожение предыдущего графика, если он существует
    if (myChart) {
        myChart.destroy();
    }
    
    // Создание нового графика
    const ctx = chartCanvas.getContext('2d');
    myChart = new Chart(ctx, {
        type: type,
        data: data,
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: title,
                    font: {
                        size: 18
                    }
                },
                legend: {
                    position: 'top',
                }
            },
            scales: type === 'scatter' ? {
                x: {
                    type: 'linear',
                    position: 'bottom'
                }
            } : {}
        }
    });
}

// Экспорт в PDF
function exportToPDF() {
    const element = document.querySelector('.charts-container');
    const opt = {
        margin: 10,
        filename: 'graph_export.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
    };
    
    // Добавление заголовка в экспорт
    const title = titleInput.value || 'График';
    const tempElement = document.createElement('div');
    tempElement.innerHTML = `<h2 style="text-align: center; margin-bottom: 20px;">${title}</h2>`;
    tempElement.appendChild(element.cloneNode(true));
    
    html2pdf().set(opt).from(tempElement).save();
}