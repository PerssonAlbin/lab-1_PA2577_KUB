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

<script>
export default {
  data() {
    return {
      mediaRecorder: null,
      audioChunks: [],
      transcribedText: '',
      inputText: '',
      audioSrc: '',
      isRecording: false,
    };
  },
  methods: {
    async startRecording() {
      this.transcribedText = '';
      this.audioChunks = [];
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        try {
          const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
          this.mediaRecorder = new MediaRecorder(stream);
          this.mediaRecorder.start();
          this.isRecording = true;

          this.mediaRecorder.ondataavailable = (e) => {
            this.audioChunks.push(e.data);
          };

          this.mediaRecorder.onstop = this.sendAudioForTranscription;
        } catch (error) {
          alert('Could not access microphone: ' + error);
        }
      } else {
        alert('Your browser does not support audio recording.');
      }
    },
    stopRecording() {
      if (this.mediaRecorder && this.isRecording) {
        this.mediaRecorder.stop();
        this.isRecording = false;
      }
    },
    async sendAudioForTranscription() {
      const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
      this.audioChunks = [];

      const formData = new FormData();
      formData.append('audio_file', audioBlob, 'recording.wav');

      try {
        const response = await this.$axios.post('/transcribe', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        this.transcribedText = response.data.transcription;
      } catch (error) {
        console.error('Error transcribing audio:', error);
        alert('Error transcribing audio.', error);
      }
    },
    async narrateText() {
      try {
        const response = await this.$axios.post('/narrate', { text: this.inputText }, {
          responseType: 'arraybuffer',
        });
        const audioBlob = new Blob([response.data], { type: 'audio/mpeg' });
        this.audioSrc = URL.createObjectURL(audioBlob);
      } catch (error) {
        console.error('Error narrating text:', error);
        alert('Error narrating text.', error);
      }
    },
  },
};
</script>

<style scoped>
/* Add any styles you need */
</style>
