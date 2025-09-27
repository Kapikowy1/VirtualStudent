const navRight = document.querySelector('.nav__rightPanel')
const navRightBtn = document.querySelector('.nav__rightBox-account')

const handleRightNav = () => {
	navRight.classList.toggle('nav__rightPanel--active')
}

const closeRightNav = event => {
	if (!navRight.contains(event.target) && !navRightBtn.contains(event.target) && !navLeftBtn.contains(event.target)) {
		navRight.classList.remove('nav__rightPanel--active')
	}
}

navRightBtn.addEventListener('click', handleRightNav)
document.addEventListener('click', closeRightNav)
