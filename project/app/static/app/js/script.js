class EmployeeForm {
	constructor() {
		this.form = document.getElementById("employeeForm");
		this.successMessage = document.getElementById("successMessage");
		this.failureMessage = document.getElementById("failureMessage");
		this.submitBtn = document.getElementById("submitBtn");
		this.clearBtn = document.getElementById("clearBtn");
		setTimeout(() => {
			this.successMessage.style.display = "none";
		}, 4000);
		setTimeout(() => {
			this.failureMessage.style.display = "none";
		}, 4000);
		this.initializeEventListeners();
		this.setMinDateForEndDate();
		
	}

	initializeEventListeners() {
		this.form.addEventListener("submit", (e) => this.handleSubmit(e));
		this.clearBtn.addEventListener("click", () => this.clearForm());

		document
			.getElementById("lastName")
			.addEventListener("blur", () => this.validateLastName());			
		document
			.getElementById("firstName")
			.addEventListener("blur", () => this.validateFirstName());
		document
			.getElementById("email")
			.addEventListener("blur", () => this.validateEmail());
		
		document
			.getElementById("course")
			.addEventListener("change", () => this.validateCourse());
		document.getElementById("startDate").addEventListener("change", () => {
			this.validateStartDate();
			this.setMinDateForEndDate();
		});
		document
			.getElementById("endDate")
			.addEventListener("change", () => this.validateEndDate());
	}

	setMinDateForEndDate() {
		const startDate = document.getElementById("startDate").value;
		if (startDate) {
			document.getElementById("endDate").min = startDate;
		}
	}

	validateLastName() {
		const lastName = document.getElementById("lastName").value.trim();
		const errorElement = document.getElementById("lastNameError");

		if (!lastName) {
			this.showError(errorElement, "Поле фамилии обязательно для заполнения");
			return false;
		}

		this.hideError(errorElement);
		return true;
	}

	validateFirstName() {
		const firstName = document.getElementById("firstName").value.trim();
		const errorElement = document.getElementById("firstNameError");

		if (!firstName) {
			this.showError(errorElement, "Поле имени обязательно для заполнения");
			return false;
		}

		this.hideError(errorElement);
		return true;
	}


	validateEmail() {
		const email = document.getElementById("email").value.trim();
		const errorElement = document.getElementById("emailError");

		if (email && !this.isValidEmail(email)) {
			this.showError(errorElement, "email должен быть корректнымыыыы");
			return false;
		}

		this.hideError(errorElement);
		return true;
	}

	validateCourse() {
		const course = document.getElementById("course").value;
		const errorElement = document.getElementById("courseError");

		if (!course) {
			this.showError(errorElement, "Выберите курс из списка");
			return false;
		}

		this.hideError(errorElement);
		return true;
	}

	validateStartDate() {
		const startDate = document.getElementById("startDate").value;
		const errorElement = document.getElementById("startDateError");

		if (!startDate) {
			this.showError(errorElement, "Укажите дату начала курса");
			return false;
		}

		this.hideError(errorElement);
		return true;
	}

	validateEndDate() {
		const startDate = document.getElementById("startDate").value;
		const endDate = document.getElementById("endDate").value;
		const errorElement = document.getElementById("endDateError");

		if (!endDate) {
			this.showError(errorElement, "Укажите дату окончания курса");
			return false;
		}

		if (startDate && endDate < startDate) {
			this.showError(
				errorElement,
				"Дата окончания не может быть раньше даты начала"
			);
			return false;
		}

		this.hideError(errorElement);
		return true;
	}

	isValidEmail(email) {
		const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
		return emailRegex.test(email);
	}

	showError(errorElement, message) {
		errorElement.textContent = message;
		errorElement.style.display = "block";
	}

	hideError(errorElement) {
		errorElement.style.display = "none";
	}

	validateForm() {
		const validations = [
			this.validateLastName(),
			this.validateFirstName(),
			this.validateEmail(),
			this.validateCourse(),
			this.validateStartDate(),
			this.validateEndDate(),
		];

		return validations.every((validation) => validation === true);
	}

	async handleSubmit(event) {
		event.preventDefault();

		if (!this.validateForm()) {
			alert("Пожалуйста, исправьте ошибки в форме");
			return;
		}

		await this.submitToServer();
	}

	async submitToServer() {
		this.submitBtn.disabled = true;
		this.submitBtn.textContent = "Отправка...";

		try {
			const lastName = document.getElementById("lastName").value.trim();
			const firstName = document.getElementById("firstName").value.trim();
			const middleName = document.getElementById("middleName").value.trim();

			let fullName = `${lastName} ${firstName}`;
			if (middleName) {
				fullName += ` ${middleName}`;
			}

			const formData = new FormData(this.form);
			formData.append("fullName", fullName);

			// console.log("Полное ФИО:", fullName);
			// console.log("Данные для отправки:", Object.fromEntries(formData));

			this.form.submit();
			
		} catch (error) {
			console.error("Ошибка при отправке данных:", error);
			alert(
				"Произошла ошибка при отправке данных. Пожалуйста, попробуйте еще раз."
			);
		} finally {
			this.submitBtn.disabled = false;
			this.submitBtn.textContent = "Отправить данные";
			
		}
	}

	showSuccessMessage() {
		this.successMessage.style.display = "block";
		setTimeout(() => {
			this.successMessage.style.display = "none";
		}, 5000);
	}

	clearForm() {
		this.form.reset();

		const errorMessages = document.querySelectorAll(".error-message");
		errorMessages.forEach((error) => (error.style.display = "none"));

		this.successMessage.style.display = "none";
	}
}

document.addEventListener("DOMContentLoaded", () => {
	new EmployeeForm();
});
