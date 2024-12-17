<!-- components/history/TimelineGroup.vue -->
<script setup>
import { computed } from 'vue';
import EventHistoryCard from './EventHistoryCard.vue';
import { AlertCircle } from 'lucide-vue-next';

const props = defineProps({
  group: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['delete', 'download']);

const formattedDate = computed(() => {
  const dateObj = new Date(props.group.created_at);
  const today = new Date();
  const yesterday = new Date(today);
  yesterday.setDate(yesterday.getDate() - 1);

  // Check if date is today or yesterday
  if (dateObj.toDateString() === today.toDateString()) {
    return 'Today';
  } else if (dateObj.toDateString() === yesterday.toDateString()) {
    return 'Yesterday';
  }

  // Get base date format with year always included
  return new Intl.DateTimeFormat('en-US', {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
    year: 'numeric'
  }).format(dateObj);
});

// Sort events by start_datetime
const sortedEvents = computed(() => {
  if (!props.group.events) return [];
  return [...props.group.events].sort((a, b) => 
    new Date(a.start_datetime) - new Date(b.start_datetime)
  );
});

// Computed property for processing status
const processingStatus = computed(() => {
  if (props.group.processing_error) {
    return {
      type: 'error',
      message: props.group.processing_error
    };
  }
  if (!props.group.processing_complete) {
    return {
      type: 'processing',
      message: 'Processing events...'
    };
  }
  return null;
});
</script>

<template>
  <div class="space-y-4">
    <!-- Group Header -->
    <div class="flex items-center gap-4">
      <h2 class="text-lg font-medium text-primary-500 dark:text-primary-100">
        {{ formattedDate }}
      </h2>
      <div class="flex-1 h-px bg-neutral-200 dark:bg-primary-700"></div>
      
      <!-- Processing Status -->
      <div v-if="processingStatus" 
           class="flex items-center gap-2 px-3 py-1 rounded-full text-sm"
           :class="{
             'bg-red-50 text-red-600 dark:bg-red-900/20 dark:text-red-400': processingStatus.type === 'error',
             'bg-yellow-50 text-yellow-600 dark:bg-yellow-900/20 dark:text-yellow-400': processingStatus.type === 'processing'
           }">
        <AlertCircle class="w-4 h-4" />
        <span>{{ processingStatus.message }}</span>
      </div>
    </div>

    <!-- Events List -->
    <div class="grid gap-4">
      <template v-for="event in sortedEvents" :key="event.id">
        <EventHistoryCard
          :event="event"
          @delete="$emit('delete', $event)"
          @download="$emit('download', $event)"
        />
      </template>
    </div>
  </div>
</template>