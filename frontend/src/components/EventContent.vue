<!-- components/EventContent.vue -->
<script setup>
import { computed } from 'vue';
import { Calendar, Lightbulb, Share2, Download, Trash2 } from 'lucide-vue-next';
import EventCard from './EventCard.vue';
import CollapsibleInfoCard from './CollapsibleInfoCard.vue';
import { downloadFile } from '../utils/downloadUtils';
import { API_ENDPOINTS } from '../config/api';
import { ToastService } from './toast';

const props = defineProps({
  event: {
    type: Object,
    required: true
  },
  showActions: {
    type: Boolean,
    default: true
  }
});

const emit = defineEmits(['update', 'export', 'share', 'download', 'delete']);

// Format event data
const formattedEvent = computed(() => ({
  startDate: new Date(props.event.start_datetime).toISOString().split('T')[0],
  startTime: new Date(props.event.start_datetime).toTimeString().slice(0, 5),
  endDate: props.event.end_datetime ? new Date(props.event.end_datetime).toISOString().split('T')[0] : null,
  endTime: props.event.end_datetime ? new Date(props.event.end_datetime).toTimeString().slice(0, 5) : null,
  location: props.event.location || '',
  venue: props.event.venue || '',
  attendees: props.event.attendees || [],
  notes: props.event.notes?.[0]?.content || ''
}));

// Get suggestions from event data or use defaults
const getSuggestions = computed(() => {
  if (!props.event?.suggestions) {
    return [
      'Send calendar invites to all attendees',
      'Prepare required materials',
      'Set up reminders'
    ];
  }

  return typeof props.event.suggestions === 'string' 
    ? props.event.suggestions.split('\n').filter(s => s.trim())
    : props.event.suggestions;
});

const handleDownload = async () => {
  try {
    const filename = `${props.event.title.toLowerCase().replace(/\s+/g, '_')}.ics`;
    const downloadUrl = API_ENDPOINTS.events.downloadIcs(props.event.id);
    
    await downloadFile(downloadUrl, filename);
    
    // You might want to emit the success for parent components
    emit('download', { success: true });
  } catch (error) {
    console.error('Failed to download event:', error);
    // You might want to emit the error for parent components to handle
    emit('download', { success: false, error });
  }
};

const handleEventDelete = async (eventId) => {
  try {
    // Emit delete event for parent to handle confirmation dialog
    emit('delete', eventId);
  } catch (error) {
    console.error('Error initiating delete:', error);
    ToastService.error(error.message || 'Failed to initiate delete');
  }
};
</script>

<template>
  <div class="group relative bg-white dark:bg-primary-800 rounded-lg shadow-sm hover:shadow-lg
               border border-neutral-200 dark:border-neutral-700 overflow-hidden
               transition-all duration-300 hover:border-accent-200 dark:hover:border-accent-700">
    <!-- Event Header -->
    <div class="p-6 border-b border-neutral-100 dark:border-neutral-700">
      <div class="space-y-4">
        <h2 class="text-xl font-bold bg-gradient-to-r from-primary-600 to-primary-500 
                   dark:from-primary-200 dark:to-primary-100 bg-clip-text text-transparent
                   group-hover:from-accent-500 group-hover:to-accent-400 
                   dark:group-hover:from-accent-300 dark:group-hover:to-accent-200
                   transition-all duration-300">
          {{ event.title }}
        </h2>
        
        <!-- Event Actions -->
        <Transition name="fade-slide">
          <div v-if="showActions"
               class="flex flex-wrap gap-3"
          >
            <button 
              @click="$emit('export')"
              class="flex items-center gap-2 px-4 py-2 bg-accent-400 text-white
                     rounded-lg shadow-sm hover:bg-accent-500 hover:shadow-md
                     transform hover:scale-102 transition-all duration-200 
                     focus:outline-none focus:ring-2 focus:ring-accent-400/50
                     active:scale-98"
            >
              <Calendar class="w-4 h-4" />
              <span>Add to Calendar</span>
            </button>

            <button 
              @click="$emit('share')"
              class="flex items-center gap-2 px-4 py-2 border border-neutral-200 dark:border-neutral-700 
                     text-neutral-700 dark:text-neutral-300 rounded-lg 
                     hover:bg-neutral-50 dark:hover:bg-neutral-700/50
                     hover:border-neutral-300 dark:hover:border-neutral-600
                     transition-all duration-200"
            >
              <Share2 class="w-4 h-4" />
              <span>Share Event</span>
            </button>

            <button 
              @click="handleDownload"
              class="flex items-center gap-2 px-4 py-2 border border-neutral-200 dark:border-neutral-700 
                     text-neutral-700 dark:text-neutral-300 rounded-lg 
                     hover:bg-neutral-50 dark:hover:bg-neutral-700/50
                     hover:border-neutral-300 dark:hover:border-neutral-600
                     transition-all duration-200"
            >
              <Download class="w-4 h-4" />
              <span>Export Details</span>
            </button>

            <button 
              @click="handleEventDelete(event.id)"
              class="flex items-center gap-2 px-4 py-2 text-sm font-medium
                     text-red-500 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/30
                     border border-red-200 dark:border-red-800 disabled:opacity-50
                     disabled:cursor-not-allowed rounded-lg shadow-sm
                     transition-all duration-200 hover:border-red-300 dark:hover:border-red-700
                     focus:outline-none focus:ring-2 focus:ring-red-400/50"
            >
              <Trash2 class="w-4 h-4" />
              <span>Delete</span>
            </button>
          </div>
        </Transition>
      </div>
    </div>

    <!-- Event Details -->
    <div class="p-6 bg-gradient-to-b from-transparent to-neutral-50/50 dark:to-primary-800/50">
      <EventCard 
        v-bind="formattedEvent"
        @update="$emit('update', $event)"
      />

      <!-- Smart Suggestions -->
      <div class="mt-6 pt-6 border-t border-neutral-100 dark:border-neutral-700">
        <CollapsibleInfoCard
          :icon="Lightbulb"
          title="Smart Suggestions"
          :content="getSuggestions"
          :initial-expanded="false"
          class="suggestions-card"
        />
      </div>
    </div>

    <!-- Decorative Corner Accent -->
    <div class="absolute top-0 right-0 w-16 h-16 overflow-hidden">
      <div class="absolute top-0 right-0 w-4 h-4 transform translate-x-2 -translate-y-2
                 bg-accent-400/10 dark:bg-accent-400/20 rounded-full blur-xl transition-all duration-300
                 group-hover:bg-accent-400/20 dark:group-hover:bg-accent-400/30 
                 group-hover:scale-150">
      </div>
    </div>
  </div>
</template>

<style>
.fade-slide-enter-active, .fade-slide-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}
.fade-slide-enter-from, .fade-slide-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
.suggestions-card :deep(.prose p) {
  word-break: break-word;
  hyphens: auto;
  max-width: 100%;
  overflow-wrap: break-word;
}
</style>