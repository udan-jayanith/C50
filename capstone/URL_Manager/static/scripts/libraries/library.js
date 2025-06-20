let urlItemTemplate = document.getElementById('url-item-template')
let urlContainer = document.querySelector('.url-list-container')

let currentUrlPageNo = 1
async function getUrls() {
	let req = await fetch(
		`${window.origin}/getUrls/${urlContainer.dataset.libraryPk}/${currentUrlPageNo}`
	)
	let json = await req.json()
	currentUrlPageNo++
	return json.list
}

let isUrlListFetching = false
let lastListLength = undefined
async function renderUrlList() {
	if (isUrlListFetching) {
		return
	} else {
		isUrlListFetching = true
	}

	if (lastListLength == 0) {
		return
	}

	let list = await getUrls()
	lastListLength = list.length
	list.forEach((obj) => {
		let urlItemEl = urlItemTemplate.content.cloneNode(true).querySelector('.url-item')
		urlItemEl.querySelector('.url-item-ico').src = getFaviconURL(obj.url)
		urlItemEl.querySelector('.url-title').innerText = obj.title
		urlItemEl.querySelector('.url-title').href = obj.url
		urlItemEl.querySelector('.url-timestamp').innerText = obj.timestamp
		let settingsOption = urlItemEl.querySelector('.settings-option')
		if (settingsOption != null) {
			settingsOption.dataset.pk = obj.pk
			settingsOption.dataset.title = obj.title
			settingsOption.dataset.url = obj.url
		}

		urlContainer.appendChild(urlItemEl)
	})

	isUrlListFetching = false
}

async function addUrlItem() {
	let urlForm = document.querySelector('.url-form')
	let title = urlForm.querySelector('.url-title').value.trim()
	let url = urlForm.querySelector('.website-url').value.trim()

	let formdata = new FormData()
	formdata.append('title', title)
	formdata.append('url', url)

	let req = await fetch(window.location.href, {
		method: 'POST',
		body: formdata,
		headers: djangoHeaders,
	})

	let json = await req.json()
	if (json.error != undefined) {
		alert(json.error)
		return
	} else {
		window.location.reload()
	}
}

let urlItemSettingsDialog = document.querySelector('.url-item-settings-dialog')
let urlItemSettingsTemplate = document.querySelector('.url-item-settings-template')

async function updateUrlItem(title, url, urlItemPk, urlEl) {
	let req = await fetch(window.location.href, {
		method: 'PUT',
		headers: djangoHeaders,
		body: JSON.stringify({
			title: title,
			url: url,
			'url-item-pk': urlItemPk,
		}),
	})

	let json = await req.json()
	if (json.error != undefined) {
		alert(json.error)
	} else {
		urlEl.href = json.url
		urlEl.innerText = json.title
	}
}

async function deleteUrlItem(urlItemPk) {
	let req = await fetch(window.location.href, {
		method: 'DELETE',
		headers: djangoHeaders,
		body: JSON.stringify({
			'url-item-pk': urlItemPk,
		}),
	})

	let json = await req.json()
	if (json.error != undefined) {
		alert(json.error)
	}
}

let librarySettingsOptionDialog = document.querySelector('.library-settings-option-dialog')
let librarySettingsOptionDialogContentTemplate = document.querySelector(
	'.library-settings-option-dialog-content-template'
).content

async function librarySettings() {
	librarySettingsOptionDialog.innerHTML = null
	librarySettingsOptionDialog.showModal()

	let librarySettingsOptionDialogContent =
		librarySettingsOptionDialogContentTemplate.cloneNode(true)
	librarySettingsOptionDialog.append(librarySettingsOptionDialogContent)

	let libraryNameInputEl = librarySettingsOptionDialog.querySelector('.library-name-input')
	let libraryDescriptionInputEl = librarySettingsOptionDialog.querySelector(
		'.library-description-input'
	)
	let libraryVisibilityModInputEl = librarySettingsOptionDialog.querySelector(
		'.library-visibility-mod-input'
	)

	let libraryNameEl = document.querySelector('.library-name')
	let libraryDescriptionEl = document.querySelector('.library-description')
	let libraryVisibilityEl = document.querySelector('.visibility-mod')

	libraryNameInputEl.value = libraryNameEl.innerText
	if (libraryDescriptionEl != null) {
		libraryDescriptionInputEl.value = libraryDescriptionEl.innerText
	}
	libraryVisibilityModInputEl.value = libraryVisibilityEl.innerText.trim().toLowerCase()

	document.querySelector('.library-close-dialog-btn').addEventListener('click', () => {
		librarySettingsOptionDialog.close()
	})

	document.querySelector('.delete-library-btn').addEventListener('click', async () => {
		let req = await fetch(`${window.location.href}/delete`)
		let json = await req.json()

		if (json.error != undefined) {
			alert(json.error)
		} else {
			window.location.assign(json.redirect)
		}
		librarySettingsOptionDialog.close()
	})

	document.querySelector('.done-library-btn').addEventListener('click', async () => {
		let formdata = new FormData()
		formdata.append('library-name', libraryNameInputEl.value)
		formdata.append('library-description', libraryDescriptionInputEl.value)
		formdata.append('visibility-mod', libraryVisibilityModInputEl.value)

		let req = await fetch(`${window.location.href}/edit`, {
			method: 'POST',
			body: formdata,
		})

		let json = await req.json()
		if (json.error != undefined) {
			alert(json.error)
		} else {
			libraryNameEl.innerText = libraryNameInputEl.value
			if (libraryDescriptionEl != null) {
				libraryDescriptionEl.innerText = libraryDescriptionInputEl.value
			}
			libraryVisibilityEl.innerText = libraryVisibilityModInputEl.value
		}
		librarySettingsOptionDialog.close()
	})
}

document.addEventListener('DOMContentLoaded', () => {
	document.querySelector('.add-url-item-btn')?.addEventListener('click', addUrlItem)

	renderUrlList()
	document.querySelector('.body-content').addEventListener('scrolled', (e) => {
		renderUrlList()
	})

	urlContainer.addEventListener('click', (e) => {
		let settingsOption = e.target.closest('.settings-option')
		if (settingsOption != null) {
			let urlItemSetting = urlItemSettingsTemplate.content
				.cloneNode(true)
				.querySelector('.url-item-settings')
			urlItemSetting.querySelector('.url-item-setting-title').value = settingsOption.dataset.title
			urlItemSetting.querySelector('.url-item-setting-url').value = settingsOption.dataset.url
			urlItemSetting.querySelector('.button-container').dataset.pk = settingsOption.dataset.pk

			urlItemSettingsDialog.innerHTML = null
			urlItemSettingsDialog.append(urlItemSetting)
			urlItemSettingsDialog.showModal()

			urlItemSettingsDialog
				.querySelector('.url-item-setting-cancel-btn')
				.addEventListener('click', () => {
					urlItemSettingsDialog.close()
				})

			let urlItemEl = settingsOption.parentNode

			urlItemSettingsDialog
				.querySelector('.url-item-setting-delete-btn')
				.addEventListener('click', () => {
					if (confirm('Are you sure you want to delete this url item.')) {
						deleteUrlItem(settingsOption.dataset.pk)
						urlItemEl.remove()
					}
					urlItemSettingsDialog.close()
				})

			urlItemSettingsDialog
				.querySelector('.url-item-setting-done-btn')
				.addEventListener('click', () => {
					updateUrlItem(
						urlItemSetting.querySelector('.url-item-setting-title').value,
						urlItemSetting.querySelector('.url-item-setting-url').value,
						settingsOption.dataset.pk,
						urlItemEl.querySelector('.url-title')
					)
					urlItemSettingsDialog.close()
				})
		}
	})

	document.querySelector('.library-settings-option')?.addEventListener('click', () => {
		librarySettings()
	})
})
