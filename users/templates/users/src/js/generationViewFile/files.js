const filterPdf = document.querySelectorAll('.files__box-pdf')

window.onload = () => {
	for (let index = 0; index < filterPdf.length; index++) {
		filterPdf[index].setAttribute('onclick', 'preview(this)')
	}
}

const previewBox = document.querySelector('.files__preview')
const previewPdf = previewBox.querySelector('iframe')
const namePdf = document.querySelector('.files__details-titleName')
const previewClose = document.querySelector('.files__details-close')
const shadow = document.querySelector('.shadow')

function preview(element) {
	document.querySelector('html').style.overflowY = 'hidden'
	let selectedPrevPdf = element.getAttribute('data-src')
	let selectedPdfName = element.getAttribute('data-name')
	namePdf.textContent = selectedPdfName
	previewPdf.src = selectedPrevPdf
	previewBox.classList.add('files__preview--show')
	shadow.classList.add('shadow--show')
	previewClose.addEventListener('click', () => {
		previewBox.classList.remove('files__preview--show')
		shadow.classList.remove('shadow--show')
		document.querySelector('html').style.overflowY = 'scroll'
	})
}
