const underlineText = document.querySelector('.termsOfUse__subsections-underline')

const tooltipText = document.querySelector('.termsOfUse__subsections-tooltip')

function showTooltip() {
	tooltipText.classList.add('termsOfUse__subsections-tooltip--show')
}

function hideTooltip() {
	tooltipText.classList.remove('termsOfUse__subsections-tooltip--show')
}

window.onload = function () {
	underlineText.addEventListener('mouseenter', showTooltip)
	underlineText.addEventListener('mouseleave', hideTooltip)
}
