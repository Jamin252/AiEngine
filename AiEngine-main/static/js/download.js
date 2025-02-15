const downloadBtn = document.getElementById('download-btn')
const downloadPopup = document.getElementById('download-popup')
const popupConfirmBtn = document.getElementById('popup-confirm-btn')
const popupCancelBtn = document.getElementById('popup-cancel-btn')

// Click the download button to display the popup
downloadBtn.addEventListener('click', () => {
	downloadPopup.classList.remove('hidden')
})

// Click the "Cancel" button to hide the popup
popupCancelBtn.addEventListener('click', () => {
	downloadPopup.classList.add('hidden')
})

// Click the "Confirm" button to process the download logic and hide the popup
popupConfirmBtn.addEventListener('click', () => {
	downloadPopup.classList.add('hidden')
	console.log('Download confirmed')
})
