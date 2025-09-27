const navLeft = document.querySelector('.nav__leftPanel')
const navLeftBtn = document.querySelector('.nav__leftBox-burger')

const handleLeftNav = () => {
	navLeft.classList.toggle('nav__leftPanel--active')
}

const closeLeftNav = event => {
	if (!navLeft.contains(event.target) && !navLeftBtn.contains(event.target)) {
		navLeft.classList.remove('nav__leftPanel--active')
	}
}

navLeftBtn.addEventListener('click', handleLeftNav)
document.addEventListener('click', closeLeftNav)
