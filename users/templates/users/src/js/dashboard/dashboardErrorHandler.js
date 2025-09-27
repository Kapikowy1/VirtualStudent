const topic = document.querySelector('#id_topic')
const purpose = document.querySelector('#id_purpose')
const sendBtn = document.querySelector('#dashboard__control-button-send')

let errorSend = true

const showError = (input, msg) => {
	const formBox = input.parentElement
	const errorMsg = formBox.querySelector('.dashboard__box-errorText')

	formBox.classList.add('dashboard__box--error')
	errorMsg.textContent = msg
}

const clearError = input => {
	const formBox = input.parentElement
	formBox.classList.remove('dashboard__box--error')
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

const checkMinLength = (input, min) => {
	if (input.value.length < min) {
		showError(input, `${input.previousElementSibling.innerText.slice(0, -1)} składa się z minimum ${min} znaków.`)
	}
}

const checkErrors = () => {
	const allInputs = document.querySelectorAll('.dashboard__box')
	let errorCount = 0

	allInputs.forEach(el => {
		if (el.classList.contains('dashboard__box--error')) {
			errorCount++
		}
	})

	if (errorCount === 0) {
		errorSend = false
	}
}

function countCharactersTopic() {
	const MIN_LENGTH = topic.minLength
	const MAX_LENGTH = topic.maxLength

	const formBox = topic.parentElement

	formBox.classList.remove('dashboard__box--error')

	const errorMsg = formBox.querySelector('.dashboard__box-errorText')

	const numerOfCharacter = topic.value.length
	const sum = MAX_LENGTH - numerOfCharacter
	const minSum = MIN_LENGTH - numerOfCharacter

	if (numerOfCharacter < MIN_LENGTH) {
		errorMsg.classList.add('dashboard__box-errorText--red')
		errorMsg.textContent = `Wymagana minimalna ilość znaków: ${minSum}`
	} else {
		errorMsg.classList.remove('dashboard__box-errorText--red')
		errorMsg.textContent = `Liczba pozostałych znaków: ${sum}`
	}
}

function countCharactersPurpose() {
	const MIN_LENGTH = purpose.minLength
	const MAX_LENGTH = purpose.maxLength

	const formBox = purpose.parentElement

	formBox.classList.remove('dashboard__box--error')

	const errorMsg = formBox.querySelector('.dashboard__box-errorText')

	const numerOfCharacter = purpose.value.length
	const sum = MAX_LENGTH - numerOfCharacter
	const minSum = MIN_LENGTH - numerOfCharacter

	if (numerOfCharacter < MIN_LENGTH) {
		errorMsg.classList.add('dashboard__box-errorText--red')
		errorMsg.textContent = `Wymagana minimalna ilość znaków: ${minSum}`
	} else {
		errorMsg.classList.remove('dashboard__box-errorText--red')
		errorMsg.textContent = `Liczba pozostałych znaków: ${sum}`
	}
}

function correctInputTopic(event) {
	const inputField = event.target // Element wywołujący zdarzenie
	const maxLength = inputField.maxLength || 150 // Maksymalna liczba znaków (domyślnie 150, jeśli brak atrybutu)
	const formBox = inputField.parentElement
	formBox.classList.remove('dashboard__box--error')
	const errorMsg = formBox.querySelector('.dashboard__box-errorText')

	function containsInvalidCharacters(text) {
		return /[^a-zA-Z0-9 ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]/.test(text) // Niedozwolone znaki (w tym spacje)
	}

	function sanitizeText(text) {
		// Usuń niedozwolone znaki
		return text.replace(/[^a-zA-Z0-9 ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]/g, '') // Dozwolone litery, cyfry i znaki specjalne
	}

	if (event.type === 'paste') {
		event.preventDefault() // Blokujemy domyślne wklejanie
		const pastedText = event.clipboardData ? event.clipboardData.getData('text') : '' // Pobieramy wklejony tekst

		// Usuń spację jako pierwszy znak, zamień polskie znaki i usuń niedozwolone
		let sanitizedText = sanitizeText(pastedText.trimStart())

		// Oblicz pozostałą przestrzeń w polu tekstowym
		const remainingLength = maxLength - inputField.value.length
		if (sanitizedText.length > remainingLength) {
			sanitizedText = sanitizedText.slice(0, remainingLength) // Przytnij tekst do dozwolonej długości
		}

		// Zamień zaznaczony tekst na oczyszczony
		const selectionStart = inputField.selectionStart
		const selectionEnd = inputField.selectionEnd
		inputField.setRangeText(
			sanitizedText, // Oczyszczony tekst
			selectionStart,
			selectionEnd,
			'end' // Ustaw kursor na końcu wklejonego tekstu
		)

		// if (containsInvalidCharacters(pastedText))
		if (pastedText !== sanitizedText) {
			// event.preventDefault() // Zablokowanie wklejania
			errorMsg.classList.add('dashboard__box--vissible')
			errorMsg.classList.add('dashboard__box-errorText--red')
			errorMsg.textContent = `Usunięto niedozwolone znaki. Dozwolone litery i cyfry.`
		} else {
			errorMsg.classList.remove('dashboard__box-errorText--red')
			errorMsg.classList.remove('dashboard__box--vissible')
			// Wywołaj funkcję liczenia znaków
			countCharactersTopic()
		}
	} else if (event.type === 'input') {
		// Usuń spację jako pierwszy znak
		if (inputField.value.startsWith(' ')) {
			inputField.value = inputField.value.trimStart()
		}

		if (containsInvalidCharacters(inputField.value)) {
			errorMsg.classList.add('dashboard__box--vissible')
			errorMsg.classList.add('dashboard__box-errorText--red')
			errorMsg.textContent = `Dozwolone litery i cyfry.`
		} else {
			errorMsg.classList.remove('dashboard__box-errorText--red')
			errorMsg.classList.remove('dashboard__box--vissible')
			// Wywołaj funkcję liczenia znaków
			countCharactersTopic()
		}

		// Sanitizuj wprowadzenie z klawiatury
		let sanitizedValue = sanitizeText(inputField.value)
		// Zaktualizuj wartość pola tekstowego
		if (inputField.value !== sanitizedValue) {
			inputField.value = sanitizedValue
		}
	} else if (event.type === 'beforeinput' && event.inputType === 'insertFromPaste') {
		// Obsługa beforeinput dla wklejania
		event.preventDefault() // Blokujemy domyślne wklejanie
		const pastedText = event.data || '' // Wklejany tekst z beforeinput

		// Usuń spację jako pierwszy znak, zamień polskie znaki i usuń niedozwolone

		let sanitizedText = sanitizeText(pastedText.trimStart())

		// Oblicz pozostałą przestrzeń w polu tekstowym
		const remainingLength = maxLength - inputField.value.length
		if (sanitizedText.length > remainingLength) {
			sanitizedText = sanitizedText.slice(0, remainingLength) // Przytnij tekst do dozwolonej długości
		}

		// Zamień zaznaczony tekst na oczyszczony
		const selectionStart = inputField.selectionStart
		const selectionEnd = inputField.selectionEnd
		inputField.setRangeText(
			sanitizedText, // Oczyszczony tekst
			selectionStart,
			selectionEnd,
			'end' // Ustaw kursor na końcu wklejonego tekstu
		)

		// if (containsInvalidCharacters(pastedText))
		if (pastedText !== sanitizedText) {
			// event.preventDefault() // Zablokowanie wklejania
			const currentInputLength = inputField.value.length // Liczba znaków obecnych w polu input
			if (inputField.value.length > 0) {
				inputField.value = inputField.value.slice(0, -currentInputLength) // Wycinamy całą zawartość pola
			}
			errorMsg.classList.add('dashboard__box--vissible')
			errorMsg.classList.add('dashboard__box-errorText--red')
			errorMsg.textContent = `Usunięto niedozwolone znaki. Dozwolone litery i cyfry.`
		} else {
			errorMsg.classList.remove('dashboard__box-errorText--red')
			errorMsg.classList.remove('dashboard__box--vissible')
			// Wywołaj funkcję liczenia znaków
			countCharactersTopic()
		}
	}
}

function correctInputPurpose(event) {
	const inputField = event.target // Element wywołujący zdarzenie
	const maxLength = inputField.maxLength || 150 // Maksymalna liczba znaków (domyślnie 150, jeśli brak atrybutu)
	const formBox = inputField.parentElement
	formBox.classList.remove('dashboard__box--error')
	const errorMsg = formBox.querySelector('.dashboard__box-errorText')

	function containsInvalidCharacters(text) {
		return /[^a-zA-Z0-9 ,.ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]/.test(text) // Niedozwolone znaki (w tym spacje)
	}

	function removeInvalidCharacters(text) {
		return text.replace(/[^a-zA-Z0-9 ,.ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]/g, '')
	}

	if (event.type === 'input') {
		// Usuń spację jako pierwszy znak
		if (inputField.value.startsWith(' ')) {
			inputField.value = inputField.value.trimStart()
		}

		if (containsInvalidCharacters(inputField.value)) {
			// Usuwanie niedozwolonych znaków
			inputField.value = inputField.value.replace(/[^a-zA-Z0-9 ,.ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]/g, '')
			errorMsg.classList.add('dashboard__box--vissible')
			errorMsg.classList.add('dashboard__box-errorText--red')
			errorMsg.textContent = `Dozwolone litery, cyfry i następujące znaki specjalne .,`
		} else {
			errorMsg.classList.remove('dashboard__box-errorText--red')
			errorMsg.classList.remove('dashboard__box--vissible')
			// Wywołaj funkcję liczenia znaków
			countCharactersPurpose()
		}
	} else if (event.type === 'paste') {
		event.preventDefault() // Blokujemy domyślne wklejanie
		const pastedText = event.clipboardData ? event.clipboardData.getData('text') : '' // Pobieramy wklejony tekst

		// Usuń niedozwolone znaki
		let sanitizedText = removeInvalidCharacters(pastedText.trimStart())
		// let sanitizedText = sanitizeText(pastedText.trimStart())

		const remainingLength = maxLength - inputField.value.length
		if (sanitizedText.length > remainingLength) {
			sanitizedText = sanitizedText.slice(0, remainingLength) // Przytnij tekst do dozwolonej długości
		}

		// Zamień zaznaczony tekst na oczyszczony
		const selectionStart = inputField.selectionStart
		const selectionEnd = inputField.selectionEnd
		inputField.setRangeText(
			sanitizedText, // Oczyszczony tekst
			selectionStart,
			selectionEnd,
			'end' // Ustaw kursor na końcu wklejonego tekstu
		)

		if (containsInvalidCharacters(pastedText)) {
			event.preventDefault() // Zablokowanie wklejania
			errorMsg.classList.add('dashboard__box--vissible')
			errorMsg.classList.add('dashboard__box-errorText--red')
			errorMsg.textContent = `Usunięto niedozwolone znaki. Dozwolone litery, cyfry i następujące znaki specjalne .,`
		} else {
			errorMsg.classList.remove('dashboard__box-errorText--red')
			errorMsg.classList.remove('dashboard__box--vissible')
			// Wywołaj funkcję liczenia znaków
			countCharactersPurpose()
		}
	} else if (event.type === 'beforeinput' && event.inputType === 'insertFromPaste') {
		event.preventDefault() // Blokujemy domyślne wklejanie
		const pastedText = event.data || '' // Wklejany tekst z beforeinput

		// Usuń niedozwolone znaki
		let sanitizedText = removeInvalidCharacters(pastedText.trimStart())

		const remainingLength = maxLength - inputField.value.length
		if (sanitizedText.length > remainingLength) {
			sanitizedText = sanitizedText.slice(0, remainingLength) // Przytnij tekst do dozwolonej długości
		}

		// Zamień zaznaczony tekst na oczyszczony
		const selectionStart = inputField.selectionStart
		const selectionEnd = inputField.selectionEnd
		inputField.setRangeText(
			sanitizedText, // Oczyszczony tekst
			selectionStart,
			selectionEnd,
			'end' // Ustaw kursor na końcu wklejonego tekstu
		)

		if (containsInvalidCharacters(pastedText)) {
			event.preventDefault() // Zablokowanie wklejania
			const currentInputLength = inputField.value.length // Liczba znaków obecnych w polu input
			if (inputField.value.length > 0) {
				inputField.value = inputField.value.slice(0, -currentInputLength) // Wycinamy całą zawartość pola
			}
			errorMsg.classList.add('dashboard__box--vissible')
			errorMsg.classList.add('dashboard__box-errorText--red')
			errorMsg.textContent = `Dozwolone litery, cyfry i następujące znaki specjalne .,`
		} else {
			errorMsg.classList.remove('dashboard__box-errorText--red')
			errorMsg.classList.remove('dashboard__box--vissible')
			// Wywołaj funkcję liczenia znaków
			countCharactersPurpose()
		}
	}
}

if (topic) {
	topic.addEventListener('beforeinput', correctInputTopic)
	topic.addEventListener('paste', correctInputTopic)
	topic.addEventListener('input', correctInputTopic)
}

if (purpose) {
	purpose.addEventListener('beforeinput', correctInputPurpose)
	purpose.addEventListener('paste', correctInputPurpose)
	purpose.addEventListener('input', correctInputPurpose)
}

sendBtn.addEventListener('click', e => {
	checkform([topic, purpose])
	checkMinLength(topic, topic.minLength)
	checkMinLength(purpose, purpose.minLength)
	checkErrors()

	if (errorSend === true) {
		e.preventDefault()
	}
})
