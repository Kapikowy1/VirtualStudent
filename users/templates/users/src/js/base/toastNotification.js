// const messagesPopup = document.querySelector('.messages--popupAcceptLog')
// const messagesPopupClose = document.querySelector('.messages-icon--close')
// const messagesContainer = document.querySelector('.messages')
const messagesContainer = document.querySelector('.messages--pop')
let timeoutId

// Funkcja do ukrywania komunikatu
function hideMessagesPopup() {
	// if (messagesPopup) {
	// 	messagesPopup.classList.add('messages--hidden')
	// }
	// else
	if (messagesContainer) {
		messagesContainer.classList.add('messages--hidden')
	}
}

// Dodaj event listener dla przycisku zamykającego, jeśli istnieje
// if (messagesPopupClose) {
// 	messagesPopupClose.addEventListener('click', () => {
// 		hideMessagesPopup()
// 		// Wyczyść timeout, aby uniknąć duplikacji działań
// 		clearTimeout(timeoutId)
// 	})
// }

// Ustaw timeout na 10 sekund, jeżeli istnieje messagesPopup
// if (messagesPopup) {
// 	timeoutId = setTimeout(() => {
// 		// hideMessagesPopup()
// 	}, 10000)
// }

if (messagesContainer) {
	timeoutId = setTimeout(() => {
		hideMessagesPopup()
	}, 10000)
}

// Dodaj event listener dla messagesContainer, jeśli messagesPopup nie istnieje
// if (!messagesPopup && messagesContainer) {
// 	messagesContainer.addEventListener('click', () => {
// 		hideMessagesPopup()
// 		clearTimeout(timeoutId)
// 	})
// }
