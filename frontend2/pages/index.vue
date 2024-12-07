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
	const audioBlob = new Blob(audioChunks.value, { type: 'audio/wav' })
	audioChunks.value = []
	const formData = new FormData()
	formData.append('audio_file', audioBlob, 'recording.wav')

	// Note: No explicit 'Content-Type' header for multipart/form-data
	const response = await $fetch('/api/transcribe', {
		method: 'POST',
		body: formData,
	})

	transcribedText.value = response.transcription
}

const narrateText = async () => {
	// Use rawResponse to handle binary data
	const response = await $fetch('/api/narrate', {
		method: 'POST',
		body: { text: inputText.value },
		responseType: 'arrayBuffer'
	})

	const audioBlob = new Blob([response], { type: 'audio/mpeg' })
	audioSrc.value = URL.createObjectURL(audioBlob)
}
</script>

<style scoped>
/* Add any styles you need */
</style>