<!-- components/common/PaginationControls.vue -->
<script setup>
defineProps({
  currentPage: {
    type: Number,
    required: true
  },
  totalPages: {
    type: Number,
    required: true
  },
  isLoading: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['page-change']);
</script>

<template>
  <div class="flex items-center justify-center space-x-4 mt-6">
    <button
      @click="emit('page-change', currentPage - 1)"
      :disabled="currentPage === 1 || isLoading"
      class="flex items-center px-4 py-2 rounded-lg text-sm font-medium
             bg-gradient-to-b from-white to-neutral-50
             dark:from-primary-700 dark:to-primary-800
             text-neutral-700 dark:text-neutral-200
             border border-neutral-200 dark:border-primary-600
             shadow-sm hover:shadow-md
             disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:shadow-sm
             transition-all duration-200 ease-in-out"
    >
      <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
      Previous
    </button>
    
    <div class="flex items-center space-x-2">
      <span class="px-3 py-1 rounded-md bg-accent-50 dark:bg-primary-900
                   text-accent-700 dark:text-accent-400 font-medium">
        {{ currentPage }}
      </span>
      <span class="text-sm text-neutral-500 dark:text-neutral-400">
        of {{ totalPages }}
      </span>
    </div>
    
    <button
      @click="emit('page-change', currentPage + 1)"
      :disabled="currentPage === totalPages || isLoading"
      class="flex items-center px-4 py-2 rounded-lg text-sm font-medium
             bg-gradient-to-b from-white to-neutral-50
             dark:from-primary-700 dark:to-primary-800
             text-neutral-700 dark:text-neutral-200
             border border-neutral-200 dark:border-primary-600
             shadow-sm hover:shadow-md
             disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:shadow-sm
             transition-all duration-200 ease-in-out"
    >
      Next
      <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
      </svg>
    </button>
  </div>
</template>