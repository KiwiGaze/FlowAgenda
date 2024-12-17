<!-- components/history/EmptyState.vue -->
<script setup>
import { Calendar, XCircle } from 'lucide-vue-next';

const props = defineProps({
  isFiltering: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['clearFilters']);
</script>

<template>
  <div class="text-center py-12">
    <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-neutral-100 dark:bg-primary-800 mb-4">
      <component 
        :is="isFiltering ? XCircle : Calendar" 
        class="w-8 h-8 text-neutral-400 dark:text-neutral-500"
      />
    </div>

    <h3 class="text-lg font-medium text-neutral-900 dark:text-neutral-100 mb-2">
      {{ isFiltering ? 'No matching events found' : 'No events yet' }}
    </h3>

    <p class="text-neutral-600 dark:text-neutral-400 max-w-md mx-auto mb-6">
      {{ isFiltering 
        ? "Try adjusting your search or filter to find what you're looking for." 
        : "When you create events, they will appear here for easy access and management."
      }}
    </p>
    
    <div class="flex justify-center">
      <template v-if="isFiltering">
        <button
          @click="$emit('clearFilters')"
          class="px-4 py-2 bg-white text-accent-400 border border-accent-400 rounded-lg hover:bg-accent-50 transition-colors inline-flex items-center gap-2"
        >
          <XCircle class="w-4 h-4" />
          Clear Filters
        </button>
      </template>
      <template v-else>
        <router-link
          to="/"
          class="px-4 py-2 bg-accent-400 text-white rounded-lg hover:bg-accent-500 transition-colors inline-flex items-center gap-2"
        >
          <Calendar class="w-4 h-4" />
          Create Event
        </router-link>
      </template>
    </div>
  </div>
</template>