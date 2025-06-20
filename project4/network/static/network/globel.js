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

function getPostWithImg(obj, userPk) {
	const card = document.createElement('div')
	card.className = 'card mb-3'

	const row = document.createElement('div')
	row.className = 'row g-0'

	const colImg = document.createElement('div')
	colImg.className = 'col-md-4'

	const img = document.createElement('img')
	img.src = obj.imgURL
	img.alt = '...'
	img.className = 'img-fluid'
	img.style.cssText = `
		height: 100%;
		object-fit: contain;
		max-height: 380px;
		min-width: 100%;
		max-width: 100%;
		display: flex;
		justify-content: center;
		align-items: center;
		border-right: 1px solid black;
	`

	colImg.appendChild(img)

	const colContent = document.createElement('div')
	colContent.className = 'col-md-8'
	if (obj.imgURL.trim() == '') {
		colContent.style.cssText = `
		width: 100%;
		`
	}

	const cardBody = document.createElement('div')
	cardBody.className = 'card-body'
	cardBody.style.cssText = `
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: flex-start;
		gap: 10px;
		width: 100%;
		height: 100%;
	`

	const headerRow = document.createElement('div')
	headerRow.style.cssText = `
		display: flex;
		flex-direction: row;
		justify-content: flex-start;
		align-items: center;
		gap: 10px;
		width: 100%;
		height: 40px;
	`

	const profileLinkEl = document.createElement('a')
	profileLinkEl.href = obj.userPage
	profileLinkEl.className = 'card-header'
	profileLinkEl.textContent = obj.user
	profileLinkEl.style.cssText =
		'width: 100%; padding: 0px; border-bottom: none; background-color: transparent;'

	headerRow.appendChild(profileLinkEl)

	if (obj.userPk === userPk) {
		const editIcon = document.createElement('i')
		editIcon.className = 'bi bi-pencil-square btn btn-secondary edit-post-btn'
		editIcon.dataset.pk = obj.pk

		const trashIcon = document.createElement('i')
		trashIcon.className =
			'bi bi-trash-fill btn btn-outline-danger delete-post-btn'
		trashIcon.dataset.pk = obj.pk

		headerRow.appendChild(editIcon)
		headerRow.appendChild(trashIcon)
	}

	const textP = document.createElement('p')
	textP.className = 'card-text'
	textP.textContent = obj.text
	textP.style.cssText = `
		margin-top: 10px;
		padding: 4px 10px 4px auto;
		text-wrap: pretty;
		box-sizing: border-box;
		width: 100%;
	`

	const footerRow = document.createElement('p')
	footerRow.className = 'card-text'
	footerRow.style.cssText = `
		display: flex;
		justify-content: flex-start;
		align-items: center;
		gap: 10px;
		width: 100%;
		margin-top: auto;
	`

	const likeBtn = document.createElement('button')
	likeBtn.className = 'btn btn-outline-danger like-btn'
	likeBtn.dataset.pk = obj.pk
	likeBtn.innerHTML = `<i class="bi bi-heart-fill"></i>`
	if (obj.liked) {
		likeBtn.classList.add('liked')
	}

	const likeText = document.createElement('medium')
	likeText.className = 'text-body-secondary like-count'
	likeText.textContent = obj.likesCount

	const dateText = document.createElement('small')
	dateText.className = 'text-body-secondary'
	dateText.style.marginLeft = 'auto'
	dateText.textContent = obj.created_at

	footerRow.appendChild(likeBtn)
	footerRow.appendChild(likeText)
	footerRow.appendChild(dateText)

	cardBody.appendChild(headerRow)
	cardBody.appendChild(textP)
	cardBody.appendChild(footerRow)

	colContent.appendChild(cardBody)

	if (obj.imgURL.trim() != '') {
		row.appendChild(colImg)
	}
	row.appendChild(colContent)

	card.appendChild(row)

	return card
}

function getPostWithText(obj, userPk) {
	return getPostWithImg(obj, userPk)
}

function redirectToProfile() {
	window.location.assign(document.body?.dataset.profile)
}

let dialogPopup = {
	open: (innerContent, width, height, unit) => {
		document.querySelector('.dialog-popup')?.remove()
		let dialog = document.createElement('dialog')
		dialog.style.cssText = `
		width: ${width}${unit};
		height: ${height}${unit};
		`
		let dialogBody = document.createElement('div')
		dialogBody.className = 'dialog-body'
		dialogBody.style.cssText = `
			width: 100%;
			height: 100%;
		`
		dialog.className = 'dialog-popup'
		if (innerContent) {
			dialogBody.append(innerContent)
		}
		dialog.append(dialogBody)
		document.body.appendChild(dialog)
		dialog.showModal()
	},

	close: () => {
		document.querySelector('.dialog-popup')?.remove()
	},
}
