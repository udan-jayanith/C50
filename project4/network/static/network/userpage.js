let followBtn = document.querySelector('.follow-btn')
if (followBtn != null) {
	followBtn.addEventListener('click', async () => {
		if (followBtn.innerText.trim() == 'Follow') {
			followBtn.innerText = 'Unfollow'
			incrementFollowerCount(1)
		} else {
            followBtn.innerText = 'Follow'
            decrementFollowerCount(1)
		}

		let formdata = new FormData()
		formdata.append('following-pk', followBtn.dataset.followingPk)
		fetch(followBtn.dataset.url, {
			method: 'POST',
			headers: djangoHeaders,
			body: formdata,
		})
	})
}

function getFollowerCount() {
    let followersCountEl = document.querySelector('.followers-count')
    return Number(followersCountEl.innerText.split(':', 2)[1].trim())
}

function incrementFollowerCount(n) {
    let followersCountEl = document.querySelector('.followers-count')
    followersCountEl.innerText = `Followers: ${getFollowerCount() + n}`
}

function decrementFollowerCount(n) {
    let followersCountEl = document.querySelector('.followers-count')
    followersCountEl.innerText = `Followers: ${getFollowerCount()-n}`
}