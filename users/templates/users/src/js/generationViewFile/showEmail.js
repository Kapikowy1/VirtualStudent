const getEmail = document.querySelector('.generationView__box-getEmail')
const emailBtn = document.querySelector('#emailToggle-icon')

const changeEyeSvg = () => {
	if (emailBtn.classList.contains('icon-tabler-eye')) {
		// Zamień na ikonę eye-off
		emailBtn.classList.remove('icon-tabler-eye')
		emailBtn.classList.add('icon-tabler-eye-off')
		const paths = emailBtn.querySelectorAll('path')
		paths[1].setAttribute('d', 'M10.585 10.587a2 2 0 0 0 2.829 2.828')
		paths[2].setAttribute(
			'd',
			'M16.681 16.673a8.717 8.717 0 0 1 -4.681 1.327c-3.6 0 -6.6 -2 -9 -6c1.272 -2.12 2.712 -3.678 4.32 -4.674m2.86 -1.146a9.055 9.055 0 0 1 1.82 -.18c3.6 0 6.6 2 9 6c-.666 1.11 -1.379 2.067 -2.138 2.87'
		)
		const newPath = document.createElementNS('http://www.w3.org/2000/svg', 'path')
		newPath.setAttribute('d', 'M3 3l18 18')
		emailBtn.appendChild(newPath)

		getEmail.type = 'text'
	} else {
		// Zamień na ikonę eye
		emailBtn.classList.remove('icon-tabler-eye-off')
		emailBtn.classList.add('icon-tabler-eye')
		const paths = emailBtn.querySelectorAll('path')
		paths[1].setAttribute('d', 'M10 12a2 2 0 1 0 4 0a2 2 0 0 0 -4 0')
		paths[2].setAttribute('d', 'M21 12c-2.4 4 -5.4 6 -9 6c-3.6 0 -6.6 -2 -9 -6c2.4 -4 5.4 -6 9 -6c3.6 0 6.6 2 9 6')
		const lastPath = emailBtn.querySelector('path:last-child')
		emailBtn.removeChild(lastPath)
		getEmail.type = 'password'
	}
}

emailBtn.addEventListener('click', changeEyeSvg)
