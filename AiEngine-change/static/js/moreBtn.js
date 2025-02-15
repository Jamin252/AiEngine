const moreBtn = document.getElementById('more-btn')
const moreMenu = document.getElementById('more-menu')

moreBtn.addEventListener('click', e => {
	e.stopPropagation()
	moreMenu.classList.toggle('hidden')
})