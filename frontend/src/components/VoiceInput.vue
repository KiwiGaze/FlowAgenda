# components/VoiceInput.vue
<script setup>
import { ref, computed } from 'vue';
import { Mic, MicOff, Loader2 } from 'lucide-vue-next';
import AudioVisualizer from './audio/AudioVisualizer.vue';

const props = defineProps({
  isRecording: Boolean,
  isProcessing: Boolean,
  visualizationType: {
    type: String,
    default: 'bars'
  }
});

const emit = defineEmits(['start-recording', 'stop-recording']);

// State
const mediaRecorder = ref(null);
const audioStream = ref(null);
const audioChunks = ref([]);

// Start recording
const startRecording = async () => {
  try {
    // Request microphone access
    audioStream.value = await navigator.mediaDevices.getUserMedia({ audio: true });
    
    // Create media recorder
    mediaRecorder.value = new MediaRecorder(audioStream.value);
    audioChunks.value = [];
    
    // Setup recorder event handlers
    mediaRecorder.value.ondataavailable = (event) => {
      audioChunks.value.push(event.data);
    };
    
    mediaRecorder.value.onstop = async () => {
      const audioBlob = new Blob(audioChunks.value, { type: 'audio/wav' });
      emit('stop-recording', audioBlob);
      
      // Clean up stream
      if (audioStream.value) {
        audioStream.value.getTracks().forEach(track => track.stop());
        audioStream.value = null;
      }
    };
    
    // Start recording
    mediaRecorder.value.start();
    emit('start-recording');
    
  } catch (error) {
    console.error('Error accessing microphone:', error);
    // Handle error appropriately
  }
};

// Stop recording
const stopRecording = () => {
  if (mediaRecorder.value && mediaRecorder.value.state === 'recording') {
    mediaRecorder.value.stop();
  }
};

// Handle recording toggle
const toggleRecording = () => {
  if (!props.isRecording && !props.isProcessing) {
    startRecording();
  } else if (props.isRecording) {
    stopRecording();
  }
};

// Dynamic classes for the recording button
const buttonClasses = computed(() => ({
  'bg-accent-500 text-white hover:bg-accent-600': !props.isRecording,
  'bg-red-500 text-white hover:bg-red-600 animate-pulse': props.isRecording,
  'opacity-50 cursor-not-allowed': props.isProcessing
}));
</script>

<template>
  <div class="voice-input-container">
    <!-- Voice Recording Button -->
    <button
      @click="toggleRecording"
      class="voice-button transform transition-all duration-300 p-4 rounded-full focus:outline-none focus:ring-2 focus:ring-accent-400"
      :class="buttonClasses"
      :disabled="props.isProcessing"
    >
      <template v-if="props.isProcessing">
        <Loader2 class="w-6 h-6 animate-spin" />
      </template>
      <template v-else>
        <Mic v-if="!props.isRecording" class="w-6 h-6" />
        <MicOff v-else class="w-6 h-6" />
      </template>
    </button>

    <!-- Audio Visualizer -->
    <div class="w-full h-16 mt-4">
        <AudioVisualizer
            :is-recording="isRecording"
            :audio-stream="audioStream"
            visualization-type="bars"
            primary-color="#60A5FA"
            secondary-color="#3B82F6"
            :sensitivity="1.2"
            :smoothing-time-constant="0.8"
        />
    </div>
  </div>
</template>

<style scoped>
.voice-input-container {
  @apply relative flex flex-col items-center gap-4;
}

.voice-button {
  @apply transform hover:scale-110 active:scale-95;
}

.voice-button:not(:disabled):hover {
  @apply shadow-lg;
}
</style>