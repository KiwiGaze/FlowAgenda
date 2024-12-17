<!-- components/ShimmerLoader.vue -->
<script setup>
const props = defineProps({
  message: {
    type: String,
    default: 'AI is processing your events'
  },
  cardsCount: {
    type: Number,
    default: 3
  }
});
</script>

<template>
  <div class="space-y-4">
    <!-- AI Message Indicator -->
    <div class="flex justify-center mb-6">
      <div class="bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 
                  px-4 py-2 rounded-full inline-flex items-center gap-2 animate-bounce
                  transition-colors duration-200">
        <svg class="w-5 h-5 animate-spin" viewBox="0 0 24 24">
          <circle 
            class="opacity-25" 
            cx="12" 
            cy="12" 
            r="10" 
            stroke="currentColor" 
            stroke-width="4" 
            fill="none"
          />
          <path 
            class="opacity-75" 
            fill="currentColor" 
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          />
        </svg>
        {{ message }}
      </div>
    </div>

    <!-- Shimmer Loading Cards -->
    <div class="animate-pulse space-y-3">
      <div v-for="i in cardsCount" :key="i" 
           class="bg-white dark:bg-gray-800 rounded-lg shadow-md dark:shadow-lg dark:shadow-gray-900/30
                  border border-neutral-200 dark:border-gray-700 overflow-hidden
                  transition-all duration-200 hover:shadow-lg dark:hover:shadow-gray-900/50">
        <div class="p-4 space-y-4">
          <!-- Title placeholder -->
          <div class="h-6 shimmer-gradient dark:shimmer-gradient-dark rounded w-3/4"></div>
          
          <!-- Action buttons placeholder -->
          <div class="flex gap-2">
            <div class="w-32 h-10 shimmer-gradient dark:shimmer-gradient-dark rounded-lg"></div>
            <div class="w-32 h-10 shimmer-gradient dark:shimmer-gradient-dark rounded-lg"></div>
          </div>
          
          <!-- Content placeholders -->
          <div class="space-y-2 pt-4">
            <div class="h-4 shimmer-gradient dark:shimmer-gradient-dark rounded w-full"></div>
            <div class="h-4 shimmer-gradient dark:shimmer-gradient-dark rounded w-5/6"></div>
            <div class="h-4 shimmer-gradient dark:shimmer-gradient-dark rounded w-4/6"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: .7;
  }
}

/* Light mode shimmer gradient */
.shimmer-gradient {
  @apply bg-gradient-to-r from-neutral-100 to-neutral-200;
  background-size: 200% 100%;
  animation: shimmer 1.5s linear infinite;
}

/* Dark mode shimmer gradient */
.shimmer-gradient-dark {
  @apply bg-gradient-to-r from-gray-700 to-gray-600;
  background-size: 200% 100%;
  animation: shimmer 1.5s linear infinite;
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

/* Smooth transitions for theme changes */
.transition-theme {
  @apply transition-all duration-200;
}

/* Enhanced dark mode shadows */
@media (prefers-color-scheme: dark) {
  .dark\:shadow-custom {
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3),
                0 2px 4px -1px rgba(0, 0, 0, 0.2);
  }
}
</style>