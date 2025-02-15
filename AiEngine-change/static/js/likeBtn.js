const likeBtn = document.getElementById('like-btn')
likeBtn.addEventListener('click', function () {
	this.classList.toggle('liked')
})
