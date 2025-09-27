const tooltipIconTopic = document.querySelector('.dashboard__tooltip-icon--topic')

const tooltipTextTopic = document.querySelector('.dashboard__tooltip-text--topic')

const tooltipIconPurpose = document.querySelector('.dashboard__tooltip-icon--purpose')

const tooltipTextPurpose = document.querySelector('.dashboard__tooltip-text--purpose')

function showTooltipTopic() {
	tooltipTextTopic.classList.add('dashboard__tooltip-text--show')
}

function hideTooltipTopic() {
	tooltipTextTopic.classList.remove('dashboard__tooltip-text--show')
}

function showTooltipPurpose() {
	tooltipTextPurpose.classList.add('dashboard__tooltip-text--show')
}

function hideTooltipPurpose() {
	tooltipTextPurpose.classList.remove('dashboard__tooltip-text--show')
}

window.onload = function () {
	tooltipIconTopic.addEventListener('mouseenter', showTooltipTopic)
	tooltipIconTopic.addEventListener('mouseleave', hideTooltipTopic)

	tooltipIconPurpose.addEventListener('mouseenter', showTooltipPurpose)
	tooltipIconPurpose.addEventListener('mouseleave', hideTooltipPurpose)
}
