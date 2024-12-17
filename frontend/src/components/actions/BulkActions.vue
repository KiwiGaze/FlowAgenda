<!-- components/BulkActions.vue -->
<script setup>
import { Calendar, Trash2, Download } from 'lucide-vue-next';

const props = defineProps({
  disabled: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['calendar', 'delete', 'export']); // Add export to emits
</script>

<template>
  <div class="sticky top-16 z-30">
    <div class="max-w-5xl mx-auto px-4 sm:px-6">
      <div class="py-3 flex flex-wrap items-center gap-3">
        <div class="flex-grow flex flex-wrap items-center gap-3 justify-end">
          <button 
            @click="$emit('calendar')"
            :disabled="disabled"
            class="flex items-center gap-2 px-4 py-2 text-sm font-medium
                   bg-accent-400 hover:bg-accent-500 disabled:opacity-50 disabled:hover:bg-accent-400
                   disabled:cursor-not-allowed text-white rounded-lg shadow-sm
                   transition-all duration-200 transform hover:scale-102 hover:shadow-md
                   focus:outline-none focus:ring-2 focus:ring-accent-400/50"
          >
            <Calendar class="w-4 h-4" />
            <span>Add All to Calendar</span>
          </button>

          <!-- Add Export All button -->
          <button 
            @click="$emit('export')"
            :disabled="disabled"
            class="flex items-center gap-2 px-4 py-2 border border-neutral-200 dark:border-neutral-700 
                     text-neutral-700 dark:text-neutral-300 rounded-lg 
                     hover:bg-neutral-50 dark:hover:bg-neutral-700/50
                     hover:border-neutral-300 dark:hover:border-neutral-600
                     transition-all duration-200"
          >
            <Download class="w-4 h-4" />
            <span>Export All</span>
          </button>
          
          <button 
            @click="$emit('delete')"
            :disabled="disabled"
            class="flex items-center gap-2 px-4 py-2 text-sm font-medium
                   text-red-500 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/30
                   border border-red-200 dark:border-red-800 disabled:opacity-50
                   disabled:cursor-not-allowed rounded-lg shadow-sm
                   transition-all duration-200 hover:border-red-300 dark:hover:border-red-700
                   focus:outline-none focus:ring-2 focus:ring-red-400/50"
          >
            <Trash2 class="w-4 h-4" />
            <span>Delete All</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>