async function addPost(e) {
	let textarea = document.querySelector('.new-post-textarea')
	let imgUrl = document.querySelector('.new-post-img-url')

	let formdata = new FormData()
	formdata.append('text', textarea.value)
	formdata.append('img-url', imgUrl.value)

	fetch(e.target.dataset.url, {
		method: 'POST',
		body: formdata,
		headers: djangoHeaders,
	})

	textarea.value = ''
	imgUrl.value = ''

	window.location.assign(e.target.dataset.profile)
}

//attach the event if the el is not null
document.querySelector('.add-post')?.addEventListener('click', (e) => addPost(e))
