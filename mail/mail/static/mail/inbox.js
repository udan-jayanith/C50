function showDiv(divName) {
	let divs = {
		emailsView: document.querySelector('#emails-view'),
		composeView: document.querySelector('#compose-view'),
		viewEmail: document.querySelector('.view-email'),
	}

	divs.emailsView.style.display = 'none'
	divs.composeView.style.display = 'none'
	divs.viewEmail.style.display = 'none'

	divs[divName].style.display = 'block'
}

document.addEventListener('DOMContentLoaded', function () {
	// Use buttons to toggle between views
	let inbox = document.querySelector('#inbox')
	inbox.addEventListener('click', (e) => load_mailbox('inbox', e.target))
	document
		.querySelector('#sent')
		.addEventListener('click', (e) => load_mailbox('sent', e.target))
	document
		.querySelector('#archived')
		.addEventListener('click', (e) => load_mailbox('archive', e.target))
	document.querySelector('#compose').addEventListener('click', compose_email)

	// By default, load the inbox
	load_mailbox('inbox', inbox)

	document.querySelector('#emails-view').addEventListener('click', (e) => {
		let emailDiv = e.target.closest('.email-div')
		if (emailDiv != null) {
			viewEmail(emailDiv.dataset.id)
		}
	})
})

function compose_email() {
	showDiv('composeView')

	// Clear out composition fields
	let recipients = document.querySelector('#compose-recipients')
	recipients.value = ''
	let subject = document.querySelector('#compose-subject')
	subject.value = ''
	let body = document.querySelector('#compose-body')
	body.value = ''

	document.querySelector('.send-btn').addEventListener('click', async (e) => {
		e.preventDefault()

		fetch('/emails', {
			method: 'POST',
			body: JSON.stringify({
				recipients: recipients.value,
				subject: subject.value,
				body: body.value,
			}),
		})
			.then((response) => response.json())
			.then((result) => {
				if (result.error != undefined) {
					alert(result.error)
				} else {
					load_mailbox('sent', document.querySelector('#sent'))
				}
			})
	})
}

async function load_mailbox(mailbox, e) {
	// Show the mailbox and hide other views
	let emailView = document.querySelector('#emails-view')
	showDiv('emailsView')

	// Show the mailbox name
	emailView.innerHTML = ``
	document.querySelector('.mailbox-name').innerText = mailbox.charAt(0).toUpperCase() + mailbox.slice(1)

	let req = await fetch(e.dataset.url)
	let json = await req.json()

	json.forEach((obj) => {
		emailView.appendChild(emailDiv(obj))
	})
}

function emailDiv(object) {
	let email = document.createElement('div')
	email.className = 'email-div'
	if (object.read) {
		email.classList.add('email-read')
	}

	email.dataset.id = object.id

	let senderName = document.createElement('div')
	senderName.className = 'sender-name'
	let senderNameText = object.sender.split('@', 1)[0]
	senderNameText = senderNameText[0].toUpperCase() + senderNameText.slice(1)
	senderName.innerText = senderNameText

	let subject = document.createElement('div')
	subject.className = 'subject-line'
	subject.innerText = object.subject

	let timestamp = document.createElement('span')
	timestamp.className = 'timestamp'
	timestamp.innerText = object.timestamp

	let firstSection = document.createElement('div')
	firstSection.className = 'first-section'
	firstSection.appendChild(senderName)
	email.appendChild(firstSection)

	let secondSection = document.createElement('div')
	secondSection.className = 'second-section'
	secondSection.appendChild(subject)
	secondSection.appendChild(timestamp)
	email.appendChild(secondSection)

	return email
}

let archiveBtnCallback = null
let replyBtnCallback = null
async function viewEmail(id) {
	let req = await fetch(`/emails/${id}`)
	let json = await req.json()
	if (json.error != undefined) {
		alert(json.error)
		return
	}

	showDiv('viewEmail')
	document.querySelector('.email-subject').innerText = json.subject
	document.querySelector('.email-sender').innerText = json.sender
	document.querySelector('.email-timestamp').innerText = json.timestamp
	document.querySelector('.recipient-list').innerText =
		json.recipients.join(', ')
	document.querySelector('.email-body').innerText = json.body

	let archiveBtn = document.querySelector('.archive-state-btn')
	archiveBtn.removeEventListener('click', archiveBtnCallback)
	if (json.archived) {
		archiveBtn.innerText = 'Unarchive'
		archiveBtnCallback = async () => {
			archiveBtn.innerText = 'Archive'
			fetch(`/emails/${id}`, {
				method: 'PUT',
				body: JSON.stringify({
					archived: false,
				}),
			})
			load_mailbox('inbox', document.querySelector('#inbox'))
		}
	} else {
		archiveBtn.innerText = 'Archive'
		archiveBtnCallback = async () => {
			archiveBtn.innerText = 'Unarchive'
			fetch(`/emails/${id}`, {
				method: 'PUT',
				body: JSON.stringify({
					archived: true,
				}),
			})
			load_mailbox('inbox', document.querySelector('#inbox'))
		}
	}
	archiveBtn.addEventListener('click', archiveBtnCallback)

	fetch(`/emails/${id}`, {
		method: 'PUT',
		body: JSON.stringify({
			read: true,
		}),
	})

	let replyBtn = document.querySelector('.reply-btn')
	replyBtn.removeEventListener('click', replyBtnCallback)
	replyBtnCallback = () => {
		compose_email()
		if (/^Re:/.exec(json.subject.trim()) == null) {
			json.subject = 'Re: ' + json.subject.trim()
		}

		let recipients = document.querySelector('#compose-recipients')
		recipients.value = json.sender
		let subject = document.querySelector('#compose-subject')
		subject.value = json.subject
		let body = document.querySelector('#compose-body')
		body.value = `\n\nOn ${json.timestamp} ${json.sender} wrote: \n${json.body}
		`
	}
	replyBtn.addEventListener('click', replyBtnCallback)
}
