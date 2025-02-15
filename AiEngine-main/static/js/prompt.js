// Get the modal
var modal = document.getElementById('promptModal')

// Get the button that opens the modal
var btn = document.getElementById('promptBtn')

// Get the <span> element that closes the modal
var span = document.getElementsByClassName('close')[0]

// When the user clicks the button, open the modal
btn.onclick = function () {
	modal.style.display = 'block'
}

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
	modal.style.display = 'none'
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
	if (event.target == modal) {
		modal.style.display = 'none'
	}
}

document.getElementById('submitPrompt').addEventListener('click', function () {
	var promptText = document.getElementById('promptInput').value
	// TODO: Send the promptText to the backend
	console.log('Prompt submitted:', promptText)
	modal.style.display = 'none'
})

function sendPrompt() {
	const promptText = document.getElementById('promptInput').value // 确保 textarea 有 id="promptText"

	fetch('/submit', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ prompt: promptText })
	})
		.then(response => response.json())
		.then(data => {
			console.log('Success:', data)
			// 在此处处理来自服务器的响应，例如显示消息
		})
		.catch(error => {
			console.error('Error:', error)
			// 在此处处理错误
		})
}
