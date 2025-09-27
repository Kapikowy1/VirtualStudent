function getQueryParam(param) {
	const urlParams = new URLSearchParams(window.location.search)
	let string
	urlParams.forEach((value, key) => {
		string = key
	})
	const doubleQuoteString = string.replace(/'/g, '"')
	const object = JSON.parse(doubleQuoteString)
	return object[param]
}

document.addEventListener('DOMContentLoaded', function () {
	document.getElementById('spot_in_queue').innerText = getQueryParam('spot_in_queue')
	document.getElementById('estimated_time').innerText = getQueryParam('estimated_time')
})
