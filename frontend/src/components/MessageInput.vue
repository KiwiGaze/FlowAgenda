<!-- components/MessageInput.vue -->
<script setup>
import { ref, computed, watch, onUnmounted } from 'vue';
import { Send, Loader2, LucidePaperclip, Globe, LucideMic } from 'lucide-vue-next';
import VoiceInput from './VoiceInput.vue';
import Tooltip from './Tooltip.vue';
import QuickActions from './actions/QuickActions.vue';

const props = defineProps({
  isLoading: {
    type: Boolean,
    default: false
  },
  maxLength: {
    type: Number,
    default: 4000
  },
  placeholder: {
    type: String,
    default: "Describe your event in natural language..."
  }
});

const emit = defineEmits(['submit', 'attachment']);

// Refs and state
const message = ref('');
const textareaRef = ref(null);
const inputContainerRef = ref(null);
const isExpanded = ref(false);
const isFocused = ref(false);
const isLLM = ref(false);
const isRecording = ref(false);
const isProcessingVoice = ref(false);
const showVoiceInput = ref(false);

// Computed properties
const charCount = computed(() => message.value.length);
const isOverLimit = computed(() => charCount.value > props.maxLength);
const showSuggestions = computed(() => isFocused.value && !props.isLoading);

// Methods
const toggleLLM = () => {
  isLLM.value = !isLLM.value;
};

const handleSubmit = () => {
  if (message.value.trim() && !props.isLoading) {
    emit('submit', {
      text: message.value,
      useLLM: isLLM.value
    });
    message.value = '';
    adjustTextareaHeight();
  }
};

const handleKeydown = (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    handleSubmit();
  }
};

const handleFocus = () => {
  isFocused.value = true;
  isExpanded.value = true;
};

const handleBlur = (event) => {
  // Only blur if clicking outside the component
  if (!event.relatedTarget?.closest('.message-input-container')) {
    isFocused.value = false;
    if (!message.value.trim()) {
      isExpanded.value = false;
    }
  }
};

const handleQuickActionSelect = (template) => {
  message.value = template;
  isExpanded.value = true;
  if (textareaRef.value) {
    textareaRef.value.focus();
    adjustTextareaHeight();
  }
};

const adjustTextareaHeight = () => {
  if (textareaRef.value) {
    textareaRef.value.style.height = 'auto';
    textareaRef.value.style.height = `${textareaRef.value.scrollHeight}px`;
  }
};

const toggleVoiceInput = () => {
  showVoiceInput.value = !showVoiceInput.value;
};

const handleStartRecording = () => {
  isRecording.value = true;
};

const handleStopRecording = async (audioBlob) => {
  try {
    isRecording.value = false;
    isProcessingVoice.value = true;

    // Create form data
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.wav');

    // Send to backend
    const response = await fetch('/api/v1/voice/process', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      throw new Error('Failed to process voice recording');
    }

    const data = await response.json();
    
    if (data.success) {
      // Append transcribed text to message
      message.value += (message.value ? ' ' : '') + data.data.transcript;
      adjustTextareaHeight();
      showVoiceInput.value = false;
    } else {
      throw new Error(data.error?.message || 'Failed to process voice recording');
    }
  } catch (error) {
    console.error('Voice processing error:', error);
    // Emit error for parent to handle
    emit('error', error.message);
  } finally {
    isProcessingVoice.value = false;
  }
};

// Handle click outside to voice input modal
const handleClickOutside = (event) => {
  if (
    showVoiceInput.value && 
    !isRecording.value &&
    inputContainerRef.value && 
    !inputContainerRef.value.contains(event.target)
  ) {
    showVoiceInput.value = false;
  }
};

// Add watch handler for showVoiceInput
watch(showVoiceInput, (newValue) => {
  if (newValue) {
    // Add event listener when modal opens
    window.addEventListener('click', handleClickOutside);
  } else {
    // Remove event listener when modal closes
    window.removeEventListener('click', handleClickOutside);
  }
});

// Add cleanup on component unmount
onUnmounted(() => {
  window.removeEventListener('click', handleClickOutside);
});

// Watch for message changes to adjust height
watch(message, adjustTextareaHeight);
</script>

<template>
  <div 
    ref="inputContainerRef"
    class="message-input-container w-full max-w-4xl mx-auto"
  >
    <!-- Main Input Area -->
    <div 
      class="relative bg-white dark:bg-surface-dark rounded-2xl shadow-sm dark:shadow-dark 
             border border-neutral-200 dark:border-neutral-700 transition-all duration-200"
      :class="{ 
        'shadow-md dark:shadow-dark-lg ring-2 ring-accent-400/20 dark:ring-accent-500/20': isExpanded,
        'hover:border-neutral-300 dark:hover:border-neutral-600': !isExpanded,
      }"
    >
      <!-- Text Input Area -->
      <div 
        class="min-h-[60px] p-4 transition-all duration-200"
        :class="{ 'min-h-[120px]': isExpanded }"
      >
        <textarea
          ref="textareaRef"
          v-model="message"
          class="w-full h-full resize-none border-none focus:ring-0 text-base 
                 text-neutral-700 dark:text-neutral-200 
                 placeholder-neutral-400 dark:placeholder-neutral-500 
                 bg-transparent transition-colors duration-200"
          :class="{ 'opacity-50': props.isLoading }"
          :placeholder="placeholder"
          :disabled="props.isLoading"
          @focus="handleFocus"
          @blur="handleBlur"
          @input="adjustTextareaHeight"
          @keydown="handleKeydown"
        ></textarea>
      </div>

      <!-- Character Count -->
      <div 
        class="px-4 py-1 text-sm text-right border-t border-neutral-100 dark:border-neutral-700
               transition-colors duration-200"
        :class="[
          isOverLimit 
            ? 'text-red-500 dark:text-red-400' 
            : 'text-neutral-500 dark:text-neutral-400'
        ]"
      >
        {{ charCount }} / {{ maxLength }}
      </div>

      <!-- Bottom Action Bar -->
      <div class="flex items-center justify-between px-4 py-2 border-t border-neutral-100 dark:border-neutral-700">
        <!-- Left Actions -->
        <div class="flex items-center gap-2">
          <Tooltip :content="isLLM ? 'Use Ollama' : 'Use Online AI'" position="top">
            <button 
              @click="toggleLLM"
              class="action-button"
              :disabled="props.isLoading"
            >
              <Globe 
                class="w-5 h-5" 
                :class="{ 'text-accent-500 dark:text-accent-400': isLLM }"
              />
            </button>
          </Tooltip>
        </div>

        <!-- Submit Button -->
        <button 
          @click="handleSubmit"
          class="px-4 py-2 bg-accent-500 text-white rounded-lg 
                 hover:bg-accent-400 dark:bg-accent-400 dark:hover:bg-accent-500 
                 transition-all duration-200 flex items-center gap-2 
                 focus:outline-none focus:ring-2 focus:ring-accent-400 focus:ring-opacity-50 
                 disabled:opacity-50 disabled:cursor-not-allowed
                 transform hover:scale-[1.02] active:scale-[0.98]"
          :disabled="!message.trim() || isOverLimit || props.isLoading"
        >
          <Loader2 v-if="props.isLoading" class="w-4 h-4 animate-spin" />
          <Send v-else class="w-4 h-4" />
          <span>Create Event</span>
        </button>
      </div>
    </div>

    <!-- Quick Actions Integration -->
    <QuickActions
      v-model="message"
      :show="showSuggestions && message.trim().length > 0"
      :is-loading="isLoading"
      @select="handleQuickActionSelect"
      class="relative z-10"
    />

    <!-- Helper Text -->
    <Transition
      enter-active-class="transition-all duration-300 ease-out"
      enter-from-class="opacity-0 transform translate-y-1"
      enter-to-class="opacity-100 transform translate-y-0"
      leave-active-class="transition-all duration-200 ease-in"
      leave-from-class="opacity-100 transform translate-y-0"
      leave-to-class="opacity-0 transform translate-y-1"
    >
      <div 
        v-if="!message.trim()"
        class="mt-4 text-center text-sm text-neutral-500 dark:text-neutral-400"
      >
        <slot name="helper">
          Press Enter to create your event
        </slot>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.message-input-container {
  contain: layout;
}

.action-button {
  @apply p-2 text-neutral-500 dark:text-neutral-400 
         hover:text-neutral-700 dark:hover:text-neutral-200 
         hover:bg-neutral-50 dark:hover:bg-neutral-700 
         rounded-lg transition-all duration-200 
         focus:outline-none focus:ring-2 focus:ring-accent-400 focus:ring-opacity-50
         transform hover:scale-110 active:scale-95;
}

.suggestions-wrapper {
  @apply mt-0 rounded-b-lg overflow-hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 
              0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

textarea {
  outline: none;
  transition: height 0.2s ease;
  max-height: 50vh;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: theme('colors.neutral.300') theme('colors.neutral.100');
}

textarea::-webkit-scrollbar {
  width: 4px;
}

textarea::-webkit-scrollbar-track {
  @apply bg-neutral-100 dark:bg-neutral-800 rounded-full;
}

textarea::-webkit-scrollbar-thumb {
  @apply bg-neutral-300 dark:bg-neutral-600 rounded-full;
}

textarea::-webkit-scrollbar-thumb:hover {
  @apply bg-neutral-400 dark:bg-neutral-500;
}

/* Voice input modal styles */
.voice-input-modal {
  filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.1));
}
</style>