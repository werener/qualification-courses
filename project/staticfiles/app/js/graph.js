// Инициализация графика
let myChart = null;

// Пример данных по умолчанию
const defaultData = {
	line: {
		labels: ["Январь", "Февраль", "Март", "Апрель", "Май"],
		datasets: [
			{
				label: "Продажи",
				data: [12, 19, 3, 5, 2],
				borderColor: "#4a6fa5",
				backgroundColor: "rgba(74, 111, 165, 0.1)",
				tension: 0.1,
			},
		],
	},
	bar: {
		labels: [
			"Управление проектами",
			"Цифровая трансформация",
			"Лидерство и командообразование",
			"Финансовый менеджмент",
			"Стратегическое планирование",
		],
		datasets: [
			{
				label: "Динамика прохождений курсов",
				data: [1, 1, 0, 0, 0],
				backgroundColor: "#6b8cbc",
			},
		],

		// labels: ['Январь', 'Февраль', 'Март', 'Апрель', 'Май'],
		// datasets: [{
		//     label: 'Доход',
		//     data: [12000, 19000, 3000, 5000, 2000],
		//     backgroundColor: '#6b8cbc'
		// }]
	},
	pie: {
		labels: [
			"Управление проектами",
			"Цифровая трансформация",
			"Лидерство и командообразование",
		],
		datasets: [
			{
				label: "Динамика прохождений курсов",
				data: [3, 2, 2],
				backgroundColor: ["#de2a1d", "#2d4f66", "x95cde2"],
			},
		],
	},
	scatter: {
		datasets: [
			{
				label: "Точечные данные",
				data: [
					{ x: 10, y: 20 },
					{ x: 15, y: 10 },
					{ x: 12, y: 15 },
					{ x: 18, y: 5 },
					{ x: 5, y: 25 },
				],
				backgroundColor: "#4a6fa5",
			},
		],
	},
};

// DOM элементы
const chartTypeSelect = document.getElementById("chartType");
const titleInput = document.getElementById("title");
const dataInput = document.getElementById("dataInput");
const generateBtn = document.getElementById("generateBtn");
const exportBtn = document.getElementById("exportBtn");
const chartCanvas = document.getElementById("myChart");

// Инициализация при загрузке страницы
document.addEventListener("DOMContentLoaded", function () {
	// Установка данных по умолчанию
	// updateDefaultData();

	// Генерация начального графика
	generateChart();

	// Обработчики событий
	chartTypeSelect.addEventListener("change", updateDefaultData);
	generateBtn.addEventListener("click", generateChart);
	exportBtn.addEventListener("click", exportToPDF);
});

// Обновление данных по умолчанию при смене типа графика
function updateDefaultData() {
	const type = chartTypeSelect.value;
	dataInput.value = JSON.stringify(defaultData[type], null, 2);

	// Установка заголовка по умолчанию
	const titles = {
		line: "Линейный график продаж",
		bar: "Столбчатая диаграмма доходов",
		pie: "Круговая диаграмма распределения",
		scatter: "Точечная диаграмма данных",
	};
}

// Генерация графика
function generateChart() {
	const type = chartTypeSelect.value;
	const title = titleInput.value;

	let data;
	try {
		data = JSON.parse(dataInput.value);
	} catch (e) {
		alert("Ошибка в формате JSON данных. Проверьте синтаксис.");
		console.error(e);
		return;
	}

	// Уничтожение предыдущего графика, если он существует
	if (myChart) {
		myChart.destroy();
	}

	// Создание нового графика
	const ctx = chartCanvas.getContext("2d");
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
						size: 18,
					},
				},
				legend: {
					position: "top",
				},
			},
			scales:
				type === "scatter"
					? {
							x: {
								type: "linear",
								position: "bottom",
							},
					  }
					: {},
		},
	});
}

// Экспорт в PDF - ИСПРАВЛЕННАЯ ВЕРСИЯ
async function exportToPDF() {
	if (!myChart) {
		alert("Сначала создайте график!");
		return;
	}

	try {
		// Показываем уведомление о начале процесса
		exportBtn.textContent = "Генерация PDF...";
		exportBtn.disabled = true;

		// Создаем временный canvas для высококачественного рендеринга
		const tempCanvas = document.createElement("canvas");
		const tempCtx = tempCanvas.getContext("2d");

		// Устанавливаем размеры для PDF
		tempCanvas.width = chartCanvas.width * 2; // Увеличиваем разрешение для PDF
		tempCanvas.height = chartCanvas.height * 2;

		// Копируем стили и данные графика
		tempCtx.fillStyle = "white";
		tempCtx.fillRect(0, 0, tempCanvas.width, tempCanvas.height);
		tempCtx.drawImage(chartCanvas, 0, 0, tempCanvas.width, tempCanvas.height);

		// Создаем HTML для экспорта
		const exportHTML = `
            <div class="pdf-export">
                <h1 class="pdf-title">${titleInput.value || "График"}</h1>
                <div class="pdf-content">
                    <img src="${tempCanvas.toDataURL(
											"image/png"
										)}" class="pdf-chart" alt="График">
                    <div class="pdf-footer">
                        <p>Сгенерировано: ${new Date().toLocaleString(
													"ru-RU"
												)}</p>
                        <p>Тип графика: ${
													chartTypeSelect.options[chartTypeSelect.selectedIndex]
														.text
												}</p>
                    </div>
                </div>
            </div>
        `;

		// Создаем временный элемент для рендеринга
		const tempElement = document.createElement("div");
		tempElement.innerHTML = exportHTML;
		document.body.appendChild(tempElement);

		// Настройки для PDF
		const opt = {
			margin: [10, 10, 10, 10],
			filename: `graph_${new Date().getTime()}.pdf`,
			image: {
				type: "jpeg",
				quality: 0.98,
			},
			html2canvas: {
				scale: 2,
				useCORS: true,
				logging: false,
			},
			jsPDF: {
				unit: "mm",
				format: "a4",
				orientation: "portrait",
			},
		};

		// Генерируем и скачиваем PDF
		await html2pdf().set(opt).from(tempElement).save();

		// Убираем временный элемент
		document.body.removeChild(tempElement);
	} catch (error) {
		console.error("Ошибка при генерации PDF:", error);
		alert(
			"Произошла ошибка при генерации PDF. Проверьте консоль для подробностей."
		);
	} finally {
		// Восстанавливаем кнопку
		exportBtn.textContent = "Экспорт в PDF";
		exportBtn.disabled = false;
	}
}

// Альтернативный метод экспорта (простой, но надежный)
function exportToPDFSimple() {
	if (!myChart) {
		alert("Сначала создайте график!");
		return;
	}

	// Создаем новое окно с содержимым для печати
	const printWindow = window.open("", "_blank");
	const title = titleInput.value || "График";
	const chartImage = chartCanvas.toDataURL("image/png");

	printWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>${title}</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    text-align: center; 
                    padding: 20px;
                }
                h1 { color: #4a6fa5; }
                img { max-width: 100%; height: auto; }
                .footer { 
                    margin-top: 20px; 
                    color: #666; 
                    font-size: 12px;
                }
                @media print {
                    body { padding: 0; }
                }
            </style>
        </head>
        <body>
            <h1>${title}</h1>
            <img src="${chartImage}" alt="График">
            <div class="footer">
                <p>Сгенерировано: ${new Date().toLocaleString("ru-RU")}</p>
                <p>Тип графика: ${
									chartTypeSelect.options[chartTypeSelect.selectedIndex].text
								}</p>
            </div>
            <script>
                window.onload = function() {
                    window.print();
                    setTimeout(function() {
                        window.close();
                    }, 500);
                };
            </script>
        </body>
        </html>
    `);
	printWindow.document.close();
}

// Заменяем основную функцию экспорта на более надежную
exportBtn.addEventListener("click", exportToPDFSimple);
