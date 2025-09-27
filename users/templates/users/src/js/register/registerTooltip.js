const tooltipIconUsername = document.querySelector('.register__tooltip-icon--username')

const tooltipTextUsername = document.querySelector('.register__tooltip-text--username')

const tooltipIconPassword = document.querySelector('.register__tooltip-icon--password')

const tooltipTextPassword = document.querySelector('.register__tooltip-text--password')

const tooltipIconConfirmPassword = document.querySelector('.register__tooltip-icon--confirmPassword')

const tooltipTextConfirmPassword = document.querySelector('.register__tooltip-text--confirmPassword')

const tooltipIconEmail = document.querySelector('.register__tooltip-icon--email')

const tooltipTextEmail = document.querySelector('.register__tooltip-text--email')

function showTooltipUsername() {
	tooltipTextUsername.classList.add('register__tooltip-text--show')
}

function hideTooltipUsername() {
	tooltipTextUsername.classList.remove('register__tooltip-text--show')
}

function showTooltipPassword() {
	tooltipTextPassword.classList.add('register__tooltip-text--show')
}

function hideTooltipPassword() {
	tooltipTextPassword.classList.remove('register__tooltip-text--show')
}

function showTooltipConfirmPassword() {
	tooltipTextConfirmPassword.classList.add('register__tooltip-text--show')
}

function hideTooltipConfirmPassword() {
	tooltipTextConfirmPassword.classList.remove('register__tooltip-text--show')
}

function showTooltipEmail() {
	tooltipTextEmail.classList.add('register__tooltip-text--show')
}

function hideTooltipEmail() {
	tooltipTextEmail.classList.remove('register__tooltip-text--show')
}

window.onload = function () {
	tooltipIconUsername.addEventListener('mouseenter', showTooltipUsername)
	tooltipIconUsername.addEventListener('mouseleave', hideTooltipUsername)

	tooltipIconPassword.addEventListener('mouseenter', showTooltipPassword)
	tooltipIconPassword.addEventListener('mouseleave', hideTooltipPassword)

	tooltipIconConfirmPassword.addEventListener('mouseenter', showTooltipConfirmPassword)
	tooltipIconConfirmPassword.addEventListener('mouseleave', hideTooltipConfirmPassword)

	tooltipIconEmail.addEventListener('mouseenter', showTooltipEmail)
	tooltipIconEmail.addEventListener('mouseleave', hideTooltipEmail)
}
