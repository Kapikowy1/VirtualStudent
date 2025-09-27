const navLogged = document.querySelector('.nav__logged')

const changeBackground = () => {
	navLogged.classList.add('nav__logged--blur')
}

changeBackground()
document.removeEventListener('DOMContentLoaded', changeBackground)
