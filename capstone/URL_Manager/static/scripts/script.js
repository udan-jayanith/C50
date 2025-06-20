function getFaviconURL(u) {
	let url = new URL(u)
	const faviconUrl = `https://www.google.com/s2/favicons?sz=256&domain=${u}`
	return faviconUrl
}

function getCookie(name) {
	let cookieValue = null
	if (document.cookie && document.cookie !== '') {
		const cookies = document.cookie.split(';')
		for (let cookie of cookies) {
			cookie = cookie.trim()
			if (cookie.startsWith(name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
				break
			}
		}
	}
	return cookieValue
}

let csrfToken = getCookie('csrftoken')
let djangoHeaders = {
	'X-CSRFToken': csrfToken,
}

const originalFetch = window.fetch
window.fetch = async (...args) => {
	;[url, options] = args
	let message = `Fetching ${url}...`
	showStatusLine(message)
	console.info(message)

	if (options != undefined && options.method != 'GET') {
		if (options.headers == undefined) {
			args[1].headers = djangoHeaders
		} else {
			args[1].headers['X-CSRFToken'] = csrfToken
		}
	}

	let req = await originalFetch(...args).finally(() => {
		hideStatusLine()
	})
	return req
}

let statusLine = document.querySelector('.status-line')
function showStatusLine(innerText) {
	statusLine.style.display = 'block'
	statusLine.innerText = innerText
}

function hideStatusLine() {
	setTimeout(() => {
		statusLine.style.display = 'none'
	}, 600)
}

document.addEventListener('DOMContentLoaded', () => {
	let bodyContent = document.querySelector('.body-content')
	bodyContent.addEventListener('scroll', (e) => {
		let scrollBottom = e.target.scrollTop + e.target.clientHeight
		let scrollableHeight = e.target.scrollHeight

		if (scrollBottom+100 >= scrollableHeight) {
			let scrolledEvent = new Event('scrolled', e)
			bodyContent.dispatchEvent(scrolledEvent)
		}
	})
	
})

