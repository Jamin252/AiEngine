const songs = [
	{
		src: '/static/song1.mp3',
		title: '失恋ソング沢山聴いて 泣いてばかりの私はもう。',
		cover: '/static/song1.jpg'
	},
	{
		src: '/static/song2.mp3',
		title: 'ハロウィンナイトパーティ (feat. Hanon & Kotoha)',
		cover: '/static/song2.jpg'
	}
]
var currentSongIndex = 0

const rangeInput = document.querySelector("input[type='range']")
// Initialize to 0%
rangeInput.style.setProperty('--range-percentage', '0%')

rangeInput.addEventListener('input', function () {
	const min = parseInt(this.min) || 0
	const max = parseInt(this.max) || 100
	const value = parseInt(this.value) || 0
	const percentage = ((value - min) / (max - min)) * 100
	this.style.setProperty('--range-percentage', `${percentage}%`)
})

// Create an Audio object without autoplay
const audio = new Audio('/static/song1.mp3')

const currentTimeEl = document.getElementById('current-time')
const remainingTimeEl = document.getElementById('remaining-time')
const progressSlider = document.getElementById('progress-slider')
const playPauseBtn = document.getElementById('play-pause-btn')

// Utility function: format seconds as mm:ss
function formatTime(seconds) {
	if (isNaN(seconds) || seconds === Infinity) {
		return ''
	}
	const mins = Math.floor(seconds / 60)
	const secs = Math.floor(seconds % 60)
	return `${mins}:${secs < 10 ? '0' : ''}${secs}`
}

// When audio metadata is loaded, initialize the time display and progress slider maximum value
audio.addEventListener('loadedmetadata', () => {
	progressSlider.max = Math.floor(audio.duration)
	currentTimeEl.textContent = formatTime(0)
	remainingTimeEl.textContent = formatTime(audio.duration)
})

// When the playback time updates, update the time display and progress slider
audio.addEventListener('timeupdate', () => {
	currentTimeEl.textContent = formatTime(audio.currentTime)
	const remaining = Math.max(audio.duration - audio.currentTime, 0)
	remainingTimeEl.textContent = formatTime(remaining)
	progressSlider.value = Math.floor(audio.currentTime)
})

audio.addEventListener('ended', () => {
	nextSong()
})

// Update playback position and time display when the user drags the slider
progressSlider.addEventListener('input', () => {
	audio.currentTime = progressSlider.value
	currentTimeEl.textContent = formatTime(audio.currentTime)
	const remaining = Math.max(audio.duration - audio.currentTime, 0)
	remainingTimeEl.textContent = formatTime(remaining)
})

disk.style.animationPlayState = 'paused'

// Play/Pause button click event
playPauseBtn.addEventListener('click', () => {
	if (audio.paused) {
		startPlay()
	} else {
		pauseSong()
	}
})

function startPlay() {
	audio
		.play()
		.then(() => {
			// Update button icon to pause state (❚❚)
			playPauseBtn.innerHTML = '&#10074;&#10074;'
			// start rotation of the disk
			disk.style.animationPlayState = 'running'
		})
		.catch(err => {
			console.error('Playback failed:', err)
		})
}

function updateCover(coverURL) {
	const disk = document.getElementById('disk')
	const img = disk.querySelector('img')
	img.src = coverURL
}
updateCover(songs[currentSongIndex].cover)

function playSong(index) {
	console.assert(index >= 0 && index < songs.length, 'Invalid song index')
	currentSongIndex = index
	updateCover(songs[currentSongIndex].cover)
	updateTitle(songs[currentSongIndex].title)
	audio.src = songs[currentSongIndex].src
	audio.load()
	startPlay()
}

function pauseSong() {
	audio.pause()
	// Update button icon to play state (▶)
	playPauseBtn.innerHTML = '&#9654;'
	// stop rotation of the disk
	disk.style.animationPlayState = 'paused'
}

function nextSong() {
	let mode = cycleModes[currentCycleModeIndex]
	if (mode === 'shuffle') {
		let nextIndex
		do {
			nextIndex = Math.floor(Math.random() * songs.length)
		} while (nextIndex === currentSongIndex && songs.length > 1)
		playSong(nextIndex)
	} else if (mode === 'single') {
		playSong(currentSongIndex)
	} else {
		// 'loop' mode
		let nextIndex = (currentSongIndex + 1) % songs.length
		playSong(nextIndex)
	}
}

function prevSong() {
	let prevIndex = (currentSongIndex - 1 + songs.length) % songs.length
	playSong(prevIndex)
}

document.getElementById('next-btn').addEventListener('click', () => {
	nextSong()
})

document.getElementById('prev-btn').addEventListener('click', () => {
	prevSong()
})
