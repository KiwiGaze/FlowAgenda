<!-- components/state/ErrorState.vue -->
<script setup>
import { AlertTriangle } from 'lucide-vue-next';

const props = defineProps({
  title: {
    type: String,
    default: 'Error'
  },
  message: {
    type: String,
    required: true
  },
  retryLabel: {
    type: String,
    default: 'Try Again'
  },
  showRetry: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['retry']);
</script>

<template>
  <Transition
    enter-active-class="transition-opacity duration-300"
    leave-active-class="transition-opacity duration-200"
    enter-from-class="opacity-0"
    leave-to-class="opacity-0"
  >
    <div class="max-w-5xl mx-auto px-4 sm:px-6 py-12">
      <div class="bg-red-50 dark:bg-red-900/30 text-red-600 dark:text-red-400 
                  p-6 rounded-lg border border-red-200 dark:border-red-800
                  shadow-sm backdrop-blur-sm">
        <div class="flex items-start gap-4">
          <div class="p-2 bg-red-100 dark:bg-red-900/50 rounded-full flex-shrink-0">
            <AlertTriangle class="w-6 h-6" />
          </div>
          <div class="flex-1 min-w-0">
            <h3 class="font-medium text-lg">{{ title }}</h3>
            <p class="mt-1 text-sm opacity-90">{{ message }}</p>
            
            <button
              v-if="showRetry"
              @click="$emit('retry')"
              class="mt-4 px-4 py-2 text-sm font-medium bg-red-100 dark:bg-red-900/50
                     text-red-600 dark:text-red-400 rounded-lg
                     hover:bg-red-200 dark:hover:bg-red-900/70
                     focus:outline-none focus:ring-2 focus:ring-red-500/50
                     transition-all duration-200"
            >
              {{ retryLabel }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>