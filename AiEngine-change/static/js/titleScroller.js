window.addEventListener('DOMContentLoaded', () => {
	const container = document.querySelector('.song-title-truncate')
	const span = container.querySelector('span')
	let originalText = span.textContent.trim()
	const gap = ' ' // A single space as separator

	// Function to update the title and restart scrolling
	function updateTitle(newTitle) {
		originalText = newTitle
		span.textContent = originalText + gap + originalText
		span.style.display = 'inline-block'

		// Recalculate the width of one text copy
		textWidth = span.offsetWidth / 2
		offset = 0 // Reset offset to start from the beginning
		span.style.transform = `translateX(0px)` // Reset transform
	}

	// Repeat the string: format "ABCDE ABCDE"
	span.textContent = originalText + gap + originalText
	// Ensure span is inline-block so that transform works correctly
	span.style.display = 'inline-block'

	// Calculate the width of one text copy (including the gap)
	let textWidth = span.offsetWidth / 2
	let offset = 0
	const speed = 30 // Scrolling speed in pixels per second

	let lastTime = null
	function animateScroll(timestamp) {
		if (!lastTime) lastTime = timestamp
		const deltaTime = (timestamp - lastTime) / 1000
		lastTime = timestamp

		offset += speed * deltaTime
		if (offset >= textWidth) {
			offset = 0
		}
		span.style.transform = `translateX(-${offset}px)`
		requestAnimationFrame(animateScroll)
	}
	requestAnimationFrame(animateScroll)

	// Attach the updateTitle function to the window object
	window.updateTitle = updateTitle
	updateTitle('失恋ソング沢山聴いて 泣いてばかりの私はもう。')
})
