const errorContainer = document.querySelector('.errorMessage')
const errorCloseBtn = document.querySelector('.errorMessage-btn')

function hideErrorMessage() {
	if (errorContainer) {
		errorContainer.classList.add('errorMessage--hidden')
	}
}
errorCloseBtn.addEventListener('click', hideErrorMessage)
