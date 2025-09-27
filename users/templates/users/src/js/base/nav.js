const nav = document.querySelector('.nav')

const handleObserver = () => {
	const currentSection = window.scrollY

	if (currentSection > 60) {
		nav.classList.add('nav--blur')
	} else {
		nav.classList.remove('nav--blur')
	}
}

// Dodajemy obserwator przewijania
window.addEventListener('scroll', handleObserver)
