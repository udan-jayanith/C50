let librariesPageNo = 1 
async function getLibraries() {
    let req = await fetch(`${window.location.href}/${librariesPageNo}`)
    let json = await req.json()
    librariesPageNo++
    return json.list
}

let libraryItemTemplate = document.querySelector('.library-item-template').content
let libraryItemContainerEl = document.querySelector('.libraries-list-container')
let lastLibraryItemListLength = undefined
async function renderLibraryItems() {
    if (lastLibraryItemListLength == 0) {
        return
    }

    let libraryItemList = await getLibraries()
    lastLibraryItemListLength = libraryItemList.length
    libraryItemList.forEach(obj => {
        let libraryItem = libraryItemTemplate.cloneNode(true)

        let libraryLinkEl = libraryItem.querySelector('.library-name')
        libraryLinkEl.innerText = obj.libraryName
        libraryLinkEl.href = `${window.location.origin}/library/${obj.libraryPk}`

        libraryItem.querySelector('.visibility-mod').innerText = obj.visibility
        libraryItem.querySelector('.creator').innerText = obj.ownerUsername
        libraryItem.querySelector(
					'.creator'
				).href = `${window.location.origin}/libraries/${obj.ownerPk}`

        libraryItemContainerEl.appendChild(libraryItem)
    });
}

async function createLibrary() {
    let libraryForm = document.querySelector('.library-form')
    if (libraryForm == null) {
        return
    }

    let libraryNameEl = document.querySelector('.library-name-input')
    let libraryDescriptionEl = document.querySelector('.library-description-input')
    let visibilityModEl = document.querySelector('.visibility-mod-input')

    let formdata = new FormData()
    formdata.append('library-name', libraryNameEl.value)
    formdata.append('library-description', libraryDescriptionEl.value)
    formdata.append('visibility-mod', visibilityModEl.value)

    let req = await fetch(window.location.href, {
        method: "POST",
        body: formdata
    })

    let json = await req.json()
    if (json.error != undefined) {
        alert(json.error)
    } else {
        window.location.assign(json.redirect)
    }
}

document.addEventListener('DOMContentLoaded', () => {
    renderLibraryItems()
    document.querySelector('.body-content').addEventListener('scrollend', () => {
        renderLibraryItems()
    })

    document.querySelector('.create-library-btn')?.addEventListener('click', () => createLibrary())
})