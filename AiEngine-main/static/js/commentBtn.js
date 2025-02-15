const commentBtn = document.getElementById('comment-btn')
commentBtn.addEventListener('click', function () {
	const commentSection = document.getElementById('comment-section')
	if (commentSection) {
		commentSection.scrollIntoView({ behavior: 'smooth' })
	}
})
