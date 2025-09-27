const username = document.querySelector('#id_username')
const password = document.querySelector('#id_password')
const passwordConfirm = document.querySelector('#id_password_confirm')
const email = document.querySelector('#id_email')
const sendBtn = document.querySelector('#register_button')

var checkbox = document.getElementById('is_consent_pop')
var hiddenInput = document.getElementById('is_consent_pop_hidden')

let errorSend = true

const showError = (input, msg) => {
	const formBox = input.parentElement
	const errorMsg = formBox.querySelector('.register__box-errorText')

	formBox.classList.add('register__box--error')
	errorMsg.textContent = msg
}

const clearError = input => {
	const formBox = input.parentElement
	formBox.classList.remove('register__box--error')
}

const checkform = input => {
	input.forEach(el => {
		if (el.value === '') {
			showError(el, el.placeholder)
		} else {
			clearError(el)
		}
	})
}

const checkLength = (input, min) => {
	if (input.value.length < min) {
		showError(
			input,
			`${input.previousElementSibling.previousElementSibling.innerText.slice(
				0,
				-1
			)} składa się z minimum ${min} znaków.`
		)
	}
}

const checkPassword = (pass1, pass2) => {
	if (pass1.value !== pass2.value) {
		showError(pass2, 'Hasła do siebie nie pasują')
	}
}

const checkMail = email => {
	const re =
		/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/

	if (re.test(email.value)) {
		clearError(email)
	} else {
		showError(email, 'E-mail jest niepoprawny')
	}
}

const checkErrors = () => {
	const allInputs = document.querySelectorAll('.register__box')
	let errorCount = 0

	allInputs.forEach(el => {
		if (el.classList.contains('register__box--error')) {
			errorCount++
		}
	})

	if (errorCount === 0) {
		errorSend = false
	}
}

function checkMaxLength(inputField, maxLength, errorMsg) {
	if (inputField.value.length >= maxLength) {
		errorMsg.classList.add('register__box--vissible')
		errorMsg.textContent = `Osiągnięto maksymalną ilość znaków: ${maxLength}`
		return true // Informuje, że osiągnięto limit
	} else {
		errorMsg.classList.remove('register__box--vissible')
		return false
	}
}

function correctInputUsername(event) {
	const inputField = event.target // Element wywołujący zdarzenie
	const maxLength = inputField.maxLength || 15
	const formBox = inputField.parentElement
	formBox.classList.remove('register__box--error')
	const errorMsg = formBox.querySelector('.register__box-errorText')

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
			errorMsg.classList.add('register__box--vissible')
			errorMsg.textContent = `Dozwolone litery i cyfry`
		} else {
			errorMsg.classList.remove('register__box--vissible')
		}
	} else if (event.type === 'paste') {
		const pastedText = event.clipboardData ? event.clipboardData.getData('text') : '' // Pobieramy wklejony tekst

		if (containsInvalidCharacters(pastedText)) {
			event.preventDefault() // Zablokowanie wklejania
			errorMsg.classList.add('register__box--vissible')
			errorMsg.textContent = `Dozwolone litery i cyfry`
		} else {
			errorMsg.classList.remove('register__box--vissible')
		}
	} else if (event.type === 'beforeinput') {
		const insertedChar = event.data

		if (insertedChar === ' ' || containsInvalidCharacters(insertedChar)) {
			// Zablokowanie spacji lub niedozwolonego znaku zanim zostanie wstawiony
			event.preventDefault()
			errorMsg.classList.add('register__box--vissible')
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
			errorMsg.classList.add('register__box--vissible')
			errorMsg.textContent = `Dozwolone litery i cyfry`
		} else {
			errorMsg.classList.remove('register__box--vissible')
		}
	}
}

function correctInputPassword(event) {
	const inputField = event.target // Element wywołujący zdarzenie
	const maxLength = inputField.maxLength || 25
	const formBox = inputField.parentElement
	formBox.classList.remove('register__box--error')
	const errorMsg = formBox.querySelector('.register__box-errorText')

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
			errorMsg.classList.add('register__box--vissible')
			errorMsg.textContent = `Dozwolone litery, cyfry i następujące znaki specjalne @#$&`
		} else {
			errorMsg.classList.remove('register__box--vissible')
		}
	} else if (event.type === 'paste') {
		const pastedText = event.clipboardData ? event.clipboardData.getData('text') : '' // Pobieramy wklejony tekst

		if (containsInvalidCharacters(pastedText)) {
			event.preventDefault() // Zablokowanie wklejania
			errorMsg.classList.add('register__box--vissible')
			errorMsg.textContent = `Dozwolone litery, cyfry i następujące znaki specjalne @#$&`
		} else {
			errorMsg.classList.remove('register__box--vissible')
		}
	} else if (event.type === 'beforeinput') {
		const insertedChar = event.data

		if (insertedChar === ' ' || containsInvalidCharacters(insertedChar)) {
			// Zablokowanie spacji lub niedozwolonego znaku zanim zostanie wstawiony
			event.preventDefault()
			errorMsg.classList.add('register__box--vissible')
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
			errorMsg.classList.add('register__box--vissible')
			errorMsg.textContent = `Dozwolone litery, cyfry i następujące znaki specjalne @#$&`
		} else {
			errorMsg.classList.remove('register__box--vissible')
		}
	}
}

function correctInputEmail(event) {
	const inputField = event.target // Element wywołujący zdarzenie
	const maxLength = inputField.maxLength || 25
	const formBox = inputField.parentElement
	formBox.classList.remove('register__box--error')
	const errorMsg = formBox.querySelector('.register__box-errorText')

	function containsInvalidCharacters(text) {
		return /[^a-zA-Z0-9._\-ąćęłńóśźżĄĆĘŁŃÓŚŹŻ@]/.test(text) // Niedozwolone znaki (w tym spacje)
	}

	if (checkMaxLength(inputField, maxLength, errorMsg)) {
		// Jeśli osiągnięto maksymalną długość, zatrzymujemy dalsze sprawdzanie
		return
	}

	if (event.type === 'input') {
		if (containsInvalidCharacters(inputField.value)) {
			// Usuwanie niedozwolonych znaków
			inputField.value = inputField.value.replace(/[^a-zA-Z0-9._\-ąćęłńóśźżĄĆĘŁŃÓŚŹŻ@]/g, '')
			errorMsg.classList.add('register__box--vissible')
			errorMsg.textContent = `Dozwolone litery, cyfry i następujące znaki specjalne .@_-`
		} else {
			errorMsg.classList.remove('register__box--vissible')
		}
	} else if (event.type === 'paste') {
		const pastedText = event.clipboardData ? event.clipboardData.getData('text') : '' // Pobieramy wklejony tekst

		if (containsInvalidCharacters(pastedText)) {
			event.preventDefault() // Zablokowanie wklejania
			errorMsg.classList.add('register__box--vissible')
			errorMsg.textContent = `Dozwolone litery, cyfry i następujące znaki specjalne .@_-`
		} else {
			errorMsg.classList.remove('register__box--vissible')
		}
	} else if (event.type === 'beforeinput') {
		const insertedChar = event.data

		if (insertedChar === ' ' || containsInvalidCharacters(insertedChar)) {
			// Zablokowanie spacji lub niedozwolonego znaku zanim zostanie wstawiony
			event.preventDefault()
			errorMsg.classList.add('register__box--vissible')
			errorMsg.textContent = `Dozwolone litery, cyfry i następujące znaki specjalne .@_-`
		}
	} else if (event.type === 'beforeinput' && event.inputType === 'insertFromPaste') {
		const pastedText = event.data
		if (containsInvalidCharacters(pastedText)) {
			event.preventDefault() // Zablokowanie wklejania
			const currentInputLength = inputField.value.length // Liczba znaków obecnych w polu input
			if (inputField.value.length > 0) {
				inputField.value = inputField.value.slice(0, -currentInputLength) // Wycinamy całą zawartość pola
			}
			errorMsg.classList.add('register__box--vissible')
			errorMsg.textContent = `Dozwolone litery, cyfry i następujące znaki specjalne .@_-`
		} else {
			errorMsg.classList.remove('register__box--vissible')
		}
	}
}

function handleCheckboxChange() {
	hiddenInput.value = checkbox.checked ? '1' : '0'
	sendBtn.classList.toggle('register__button--disabled')

	if (sendBtn.hasAttribute('disabled')) {
		sendBtn.removeAttribute('disabled') // Usuwa atrybut
	} else {
		sendBtn.setAttribute('disabled', 'true') // Dodaje atrybut
	}
}

checkbox.addEventListener('change', handleCheckboxChange)
window.onload = handleCheckboxChange // Ensure correct initial state

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

if (passwordConfirm) {
	passwordConfirm.addEventListener('beforeinput', correctInputPassword)
	passwordConfirm.addEventListener('paste', correctInputPassword)
	passwordConfirm.addEventListener('input', correctInputPassword)
}

if (email) {
	email.addEventListener('beforeinput', correctInputEmail)
	email.addEventListener('paste', correctInputEmail)
	email.addEventListener('input', correctInputEmail)
}

sendBtn.addEventListener('click', e => {
	checkform([username, password, passwordConfirm, email])
	checkLength(username, 3)
	checkLength(password, 6)
	checkPassword(password, passwordConfirm)
	checkMail(email)
	checkErrors()

	if (errorSend === true) {
		e.preventDefault()
	}
})
