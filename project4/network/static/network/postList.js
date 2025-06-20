let nextPostsCount = 1
let lastPostListLength = 1
async function getPost() {
	let formdata = new FormData()
	formdata.append('s-t', nextPostsCount)
	let req = await fetch(
		document.querySelector('.posts-container').dataset.url,
		{
			method: 'POST',
			body: formdata,
			headers: djangoHeaders,
		}
	)
	let json = await req.json()
	if (json.error != undefined && json.error == 'end') {
		return
	}

	renderPostList(json.postLists, json.userPk)

	if (json.postLists.length < 10) {
		document.querySelector('.next-btn')?.classList.add('disabled')
	} else {
		document.querySelector('.next-btn')?.classList.remove('disabled')
	}

	if (nextPostsCount > 10) {
		document.querySelector('.previous-btn')?.classList.remove('disabled')
	} else {
		document.querySelector('.previous-btn')?.classList.add('disabled')
	}

	lastPostListLength = json.postLists.length
	nextPostsCount += lastPostListLength
}

document.querySelector('.next-btn')?.addEventListener('click', () => {
	getPost()
})

document.querySelector('.previous-btn')?.addEventListener('click', () => {
	nextPostsCount -= 10 + lastPostListLength
	if (nextPostsCount <= 0) {
		nextPostsCount = 1
	}
	getPost()
})

document.addEventListener('DOMContentLoaded', () => {
	getPost()
})

function renderPostList(list, userPk) {
	let postListContainer = document.querySelector('.posts-container')
	postListContainer.innerHTML = null
	list.forEach((obj) => {
		if (obj.imgURL == undefined || obj.imgURL.trim() == '') {
			postListContainer.appendChild(getPostWithText(obj, userPk))
		} else {
			postListContainer.appendChild(getPostWithImg(obj, userPk))
		}
	})
	window.scrollTo(0, 0)
}

document.querySelector('.posts-container')?.addEventListener('click', (e) => {
	let likeBtn = e.target.closest('.like-btn')
	let deleteBtn = e.target.closest('.delete-post-btn')
	let editBtn = e.target.closest('.edit-post-btn')
	if (likeBtn != null) {
		likePost(likeBtn)
	} else if (deleteBtn != null) {
		deletePost(deleteBtn)
	} else if (editBtn != null) {
		editPost(editBtn.dataset.pk)
	}
})

function changeLikeCount(likeEl, n) {
	let currentLikeCount = Number(likeEl.innerText.trim())
	likeEl.innerText = currentLikeCount + n
}

async function likePost(likeBtn) {
	let req = await fetch(
		`${window.location.origin}/post/${likeBtn.dataset.pk}/like`
	)
	let json = await req.json()
	if (json.error != undefined) {
		alert(json.error)
	} else {
		let likeCountEl = likeBtn.parentElement.querySelector('.like-count')
		if (likeBtn.classList.contains('liked')) {
			likeBtn.classList.remove('liked')
			changeLikeCount(likeCountEl, -1)
		} else {
			likeBtn.classList.add('liked')
			changeLikeCount(likeCountEl, 1)
		}
	}
}

async function deletePost(deleteBtn) {
	if (!confirm('Are you sure you want to delete this post.')) {
		return
	}

	let req = await fetch(
		`${window.location.origin}/post/${deleteBtn.dataset.pk}/delete`
	)
	let json = await req.json()
	if (json.error != undefined) {
		alert(json.error)
	} else {
		redirectToProfile()
	}
}

async function editPost(pk) {
	let req = await fetch(`${window.location.origin}/post/${pk}/edit`, {
		method: 'GET',
		headers: djangoHeaders,
	})
	let json = await req.json()

	const container = document.createElement('div')
	container.className = 'mb-3'
	// Label for textarea
	const textareaLabel = document.createElement('label')
	textareaLabel.setAttribute('for', 'exampleFormControlTextarea1')
	textareaLabel.className = 'form-label'
	textareaLabel.textContent = 'Edit post'
	container.appendChild(textareaLabel)

	// Textarea
	const textarea = document.createElement('textarea')
	textarea.className = 'form-control edit-post-textarea'
	textarea.id = 'exampleFormControlTextarea1'
	textarea.rows = 3
	textarea.placeholder = "What's on your mind."
	textarea.innerText = json.text
	container.appendChild(textarea)

	// Inner div for image input
	const imageDiv = document.createElement('div')
	imageDiv.className = 'mb-3'

	// Label for image input
	const imageLabel = document.createElement('label')
	imageLabel.setAttribute('for', 'exampleFormControlInput1')
	imageLabel.className = 'form-label'
	imageLabel.textContent = 'Image URL'
	imageDiv.appendChild(imageLabel)

	// Input field
	const imageInput = document.createElement('input')
	imageInput.type = 'url'
	imageInput.className = 'form-control edit-post-img-url'
	imageInput.id = 'exampleFormControlInput1'
	imageInput.placeholder = 'https://www.unshplash.com/network.jpg'
	imageInput.value = json.imgURL
	imageDiv.appendChild(imageInput)

	container.appendChild(imageDiv)

	// Post button
	const doneButton = document.createElement('button')
	doneButton.className = 'btn btn-primary mb-3'
	doneButton.textContent = 'Done'
	doneButton.addEventListener('click', async () => {
		let formdata = new FormData()
		formdata.append('text', textarea.value)
		formdata.append('img-url', imageInput.value)
		let req = await fetch(`${window.location.origin}/post/${pk}/edit`, {
			method: 'POST',
			headers: djangoHeaders,
			body: formdata
		})

		let json = await req.json()
		if (json.error != undefined) {
			alert(json.error)
		}
		
		redirectToProfile()
		dialogPopup.close()
	})

	const cancelButton = document.createElement('button')
	cancelButton.className = 'btn btn-secondary mb-3'
	cancelButton.textContent = 'Cancel'
	cancelButton.style.cssText = `
		margin-left: 10px;
	`
	cancelButton.addEventListener('click', () => {
		dialogPopup.close()
	})

	container.appendChild(doneButton)
	container.appendChild(cancelButton)

	// Then append it to the document
	document.body.appendChild(container)

	dialogPopup.open(container, 60, 40, '%')
}

