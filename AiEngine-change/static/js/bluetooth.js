const connectBtn = document.getElementById('connect-btn')
const bluetoothPopup = document.getElementById('bluetooth-popup')
const bluetoothConfirmBtn = document.getElementById('bluetooth-confirm-btn')
const bluetoothCancelBtn = document.getElementById('bluetooth-cancel-btn')

connectBtn.addEventListener('click', () => {
	bluetoothPopup.classList.remove('hidden')
})

bluetoothCancelBtn.addEventListener('click', () => {
	bluetoothPopup.classList.add('hidden')
})

bluetoothConfirmBtn.addEventListener('click', () => {
	bluetoothPopup.classList.add('hidden')
	console.log('Bluetooth connection confirmed')
})
