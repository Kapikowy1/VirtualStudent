const username = document.querySelector('#id_username')
const password = document.querySelector('#id_password')

function checkMaxLength(inputField, maxLength, errorMsg) {
	if (inputField.value.length >= maxLength) {
		errorMsg.classList.add('login__box--vissible')
		errorMsg.textContent = `Osiągnięto maksymalną ilość znaków: ${maxLength}`
		return true // Informuje, że osiągnięto limit
	} else {
		errorMsg.classList.remove('login__box--vissible')
		return false
	}
}

function correctInputUsername(event) {
	const inputField = event.target // Element wywołujący zdarzenie
	const maxLength = inputField.maxLength || 15
	const formBox = inputField.parentElement
	formBox.classList.remove('login__box--error')
	const errorMsg = formBox.querySelector('.login__box-errorText')

	function containsInvalidCharacters(text) {
		return /[^a-zA-Z0-9ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]/.test(text) // Niedozwolone znaki (w tym spacje)
	}

	if (checkMaxLength(inputField, maxLength, errorMsg)) {
		// Jeśli osiągnięto maksymalną długość, zatrzymujemy dalsze sprawdzanie
		return
	}

	if (event.type === 'input') {
		if (containsInvalidCharacters(inputField.value)) {
			// Usuwanie niedozwolonych znaków
			inputField.value = inputField.value.replace(/[^a-zA-Z0-9 ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]/g, '')
			errorMsg.classList.add('login__box--vissible')
			errorMsg.textContent = `Dozwolone litery i cyfry`
		} else {
			errorMsg.classList.remove('login__box--vissible')
		}
	} else if (event.type === 'paste') {
		const pastedText = event.clipboardData ? event.clipboardData.getData('text') : '' // Pobieramy wklejony tekst

		if (containsInvalidCharacters(pastedText)) {
			event.preventDefault() // Zablokowanie wklejania
			errorMsg.classList.add('login__box--vissible')
			errorMsg.textContent = `Dozwolone litery i cyfry`
		} else {
			errorMsg.classList.remove('login__box--vissible')
		}
	} else if (event.type === 'beforeinput') {
		const insertedChar = event.data

		if (insertedChar === ' ' || containsInvalidCharacters(insertedChar)) {
			// Zablokowanie spacji lub niedozwolonego znaku zanim zostanie wstawiony
			event.preventDefault()
			errorMsg.classList.add('login__box--vissible')
			errorMsg.textContent = `Dozwolone litery i cyfry`
		}
	} else if (event.type === 'beforeinput' && event.inputType === 'insertFromPaste') {
		const pastedText = event.data
		if (containsInvalidCharacters(pastedText)) {
			event.preventDefault() // Zablokowanie wklejania
			const currentInputLength = inputField.value.length // Liczba znaków obecnych w polu input
			if (inputField.value.length > 0) {
				inputField.value = inputField.value.slice(0, -currentInputLength) // Wycinamy całą zawartość pola
			}
			errorMsg.classList.add('login__box--vissible')
			errorMsg.textContent = `Dozwolone litery i cyfry`
		} else {
			errorMsg.classList.remove('login__box--vissible')
		}
	}
}

function correctInputPassword(event) {
	const inputField = event.target // Element wywołujący zdarzenie
	const maxLength = inputField.maxLength || 15
	const formBox = inputField.parentElement
	formBox.classList.remove('login__box--error')
	const errorMsg = formBox.querySelector('.login__box-errorText')

	function containsInvalidCharacters(text) {
		return /[^a-zA-Z0-9ąćęłńóśźżĄĆĘŁŃÓŚŹŻ@#$&]/.test(text) // Niedozwolone znaki (w tym spacje)
	}

	if (checkMaxLength(inputField, maxLength, errorMsg)) {
		// Jeśli osiągnięto maksymalną długość, zatrzymujemy dalsze sprawdzanie
		return
	}

	if (event.type === 'input') {
		if (containsInvalidCharacters(inputField.value)) {
			// Usuwanie niedozwolonych znaków
			inputField.value = inputField.value.replace(/[^a-zA-Z0-9 ąćęłńóśźżĄĆĘŁŃÓŚŹŻ@#$&]/g, '')
			errorMsg.classList.add('login__box--vissible')
			errorMsg.textContent = `Dozwolone litery, cyfry i następujące znaki specjalne @#$&`
		} else {
			errorMsg.classList.remove('login__box--vissible')
		}
	} else if (event.type === 'paste') {
		const pastedText = event.clipboardData ? event.clipboardData.getData('text') : '' // Pobieramy wklejony tekst

		if (containsInvalidCharacters(pastedText)) {
			event.preventDefault() // Zablokowanie wklejania
			errorMsg.classList.add('login__box--vissible')
			errorMsg.textContent = `Dozwolone litery, cyfry i następujące znaki specjalne @#$&`
		} else {
			errorMsg.classList.remove('login__box--vissible')
		}
	} else if (event.type === 'beforeinput') {
		const insertedChar = event.data

		if (insertedChar === ' ' || containsInvalidCharacters(insertedChar)) {
			// Zablokowanie spacji lub niedozwolonego znaku zanim zostanie wstawiony
			event.preventDefault()
			errorMsg.classList.add('login__box--vissible')
			errorMsg.textContent = `Dozwolone litery, cyfry i następujące znaki specjalne @#$&`
		}
	} else if (event.type === 'beforeinput' && event.inputType === 'insertFromPaste') {
		const pastedText = event.data
		if (containsInvalidCharacters(pastedText)) {
			event.preventDefault() // Zablokowanie wklejania
			const currentInputLength = inputField.value.length // Liczba znaków obecnych w polu input
			if (inputField.value.length > 0) {
				inputField.value = inputField.value.slice(0, -currentInputLength) // Wycinamy całą zawartość pola
			}
			errorMsg.classList.add('login__box--vissible')
			errorMsg.textContent = `Dozwolone litery, cyfry i następujące znaki specjalne @#$&`
		} else {
			errorMsg.classList.remove('login__box--vissible')
		}
	}
}

if (username) {
	username.addEventListener('beforeinput', correctInputUsername)
	username.addEventListener('paste', correctInputUsername)
	username.addEventListener('input', correctInputUsername)
}

if (password) {
	password.addEventListener('beforeinput', correctInputPassword)
	password.addEventListener('paste', correctInputPassword)
	password.addEventListener('input', correctInputPassword)
}
