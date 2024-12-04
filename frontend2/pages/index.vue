<template>
	<div>
		<h1>Transcription and Narration</h1>
		<div>
			<h2>Transcribe Audio</h2>
			<button @click="startRecording">Start Recording</button>
			<button @click="stopRecording" :disabled="!isRecording">Stop Recording</button>
			<p v-if="transcribedText">Transcribed Text: {{ transcribedText }}</p>
		</div>
		<div>
			<h2>Narrate Text</h2>
			<textarea v-model="inputText" placeholder="Enter text to narrate"></textarea>
			<button @click="narrateText">Narrate</button>
			<audio v-if="audioSrc" :src="audioSrc" controls></audio>
		</div>
	</div>
</template>

<script setup>
import { ref } from 'vue'
import { useFetch } from '#app'

const mediaRecorder = ref(null)
const audioChunks = ref([])
const transcribedText = ref('')
const inputText = ref('')
const audioSrc = ref('')
const isRecording = ref(false)

const startRecording = async () => {
	transcribedText.value = ''
	audioChunks.value = []
	if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
		try {
			const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
			mediaRecorder.value = new MediaRecorder(stream)
			mediaRecorder.value.start()
			isRecording.value = true

			mediaRecorder.value.ondataavailable = (e) => {
				audioChunks.value.push(e.data)
			}

			mediaRecorder.value.onstop = sendAudioForTranscription
		} catch (error) {
			alert('Could not access microphone: ' + error)
		}
	} else {
		alert('Your browser does not support audio recording.')
	}
}

const stopRecording = () => {
	if (mediaRecorder.value && isRecording.value) {
		mediaRecorder.value.stop()
		isRecording.value = false
	}
}

const sendAudioForTranscription = async () => {
	const audioBlob = new Blob(audioChunks.value, { type: 'audio/mpeg' })
	audioChunks.value = []

	const formData = new FormData()
	formData.append('audio_file', audioBlob, 'recording.mpeg')

	try {
		const { data } = await useFetch('/api/transcribe', {
			method: 'POST',
			body: formData,
			headers: {
				'Content-Type': 'multipart/form-data',
			},
		})

		transcribedText.value = data.value.transcription
	} catch (error) {
		console.error('Error transcribing audio:', error)
		alert('Error transcribing audio.')
	}
}

const narrateText = async () => {
	try {
		const { data } = await useFetch('/api/narrate', {
			method: 'POST',
			body: JSON.stringify({ text: inputText.value }),
			headers: {
				'Content-Type': 'application/json',
			},
			responseType: 'blob'
		})

		audioSrc.value = URL.createObjectURL(data.value)
	} catch (error) {
		console.error('Error narrating text:', error)
		alert('Error narrating text.')
	}
}

const base64ToBlob = (base64, type) => {
	const byteCharacters = atob(base64)
	const byteNumbers = new Array(byteCharacters.length)
	for (let i = 0; i < byteCharacters.length; i++) {
		byteNumbers[i] = byteCharacters.charCodeAt(i)
	}
	const byteArray = new Uint8Array(byteNumbers)
	return new Blob([byteArray], { type: type })
}
</script>

<style scoped>
/* Add any styles you need */
</style>
