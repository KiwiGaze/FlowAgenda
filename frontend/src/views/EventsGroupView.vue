<!-- views/EventsGroupView.vue -->
<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ToastService } from '@/components/toast';
import { useEventsGroupStore } from '../stores/eventsGroupStore';
import HeaderActions from '../components/actions/HeaderActions.vue';
import BulkActions from '../components/actions/BulkActions.vue';
import EventContent from '../components/EventContent.vue';
import LoadingState from '../components/state/LoadingState.vue';
import ErrorState from '../components/state/ErrorState.vue';
import ConfirmationDialog from '../components/dialog/ConfirmationDialog.vue';
import { API_ENDPOINTS } from '../config/api';
import { downloadFile } from '../utils/downloadUtils';

const route = useRoute();
const router = useRouter();
const eventsGroupStore = useEventsGroupStore();

// State
const isLoading = ref(false);
const searchQuery = ref('');
const pollingInterval = ref(null);
const loadingType = ref('default');
const showDeleteConfirmation = ref(false);
const showBulkDeleteConfirmation = ref(false);

const showExportConfirmation = ref(false);
const exportConfirmationMessage = ref('');

// Add this with other state variables at the top
const showSingleDeleteConfirmation = ref(false);
const eventToDelete = ref(null);

// Computed
const showContent = computed(() => {
  return !eventsGroupStore.isLoading && 
         !eventsGroupStore.isProcessing && 
         !eventsGroupStore.hasError && 
         eventsGroupStore.currentGroup?.events?.length > 0;
});

const filteredEvents = computed(() => {
  if (!eventsGroupStore.currentGroup?.events) return [];
  if (!searchQuery.value) return eventsGroupStore.currentGroup.events;
  
  const query = searchQuery.value.toLowerCase();
  return eventsGroupStore.currentGroup.events.filter(event => 
    event.title.toLowerCase().includes(query) ||
    event.location?.toLowerCase().includes(query) ||
    event.venue?.toLowerCase().includes(query)
  );
});

const eventCountDisplay = computed(() => {
  const count = eventsGroupStore.currentGroup?.events?.length || 0;
  return `${count} ${count === 1 ? 'Event' : 'Events'}`;
});

// Actions
const handleBack = () => {
  router.back();
};

const handleEventUpdate = async (eventId, updates) => {
  try {
    const event = filteredEvents.value.find(e => e.id === eventId);
    if (event) {
      Object.assign(event, updates);
      // Implement API update here
      ToastService.success('Event updated successfully');
    }
  } catch (error) {
    console.error('Error updating event:', error);
    ToastService.error('Failed to update event');
  }
};

const handleAddToCalendar = async (event) => {
  try {
    loadingType.value = 'calendar';
    isLoading.value = true;
    // Implement calendar integration here
    await new Promise(resolve => setTimeout(resolve, 1000)); // Simulated delay
    ToastService.success('Event added to calendar');
  } catch (error) {
    console.error('Error adding event to calendar:', error);
    ToastService.error('Failed to add event to calendar');
  } finally {
    isLoading.value = false;
    loadingType.value = 'default';
  }
};

const handleAddAllToCalendar = async () => {
  try {
    loadingType.value = 'calendar';
    isLoading.value = true;
    // Implement bulk calendar integration here
    await Promise.all(
      filteredEvents.value.map(event => handleAddToCalendar(event))
    );
    ToastService.success('All events added to calendar');
  } catch (error) {
    console.error('Error adding events to calendar:', error);
    ToastService.error('Failed to add events to calendar');
  } finally {
    isLoading.value = false;
    loadingType.value = 'default';
  }
};

const confirmBulkDelete = () => {
  showBulkDeleteConfirmation.value = true;
};

const handleBulkDelete = async () => {
  try {
    showBulkDeleteConfirmation.value = false;
    loadingType.value = 'delete';
    isLoading.value = true;
    
    // Delete all filtered events sequentially
    await Promise.all(
      filteredEvents.value.map(event => 
        eventsGroupStore.deleteEvent(event.id)
      )
    );
    
    ToastService.success('All events deleted');
    
    // If no events left, redirect to input page
    if (eventsGroupStore.currentGroup?.events?.length === 0) {
      router.push({ name: 'input' });
    }
  } catch (error) {
    console.error('Error deleting events:', error);
    ToastService.error('Failed to delete events');
  } finally {
    isLoading.value = false;
    loadingType.value = 'default';
  }
};

const confirmEventDelete = (eventId) => {
  eventToDelete.value = eventId;
  showSingleDeleteConfirmation.value = true;
};

const handleEventDelete = async () => {
  try {
    showSingleDeleteConfirmation.value = false;
    loadingType.value = 'delete';
    isLoading.value = true;

    await eventsGroupStore.deleteEvent(eventToDelete.value);
    ToastService.success('Event deleted successfully');

    // Reset the event to delete
    eventToDelete.value = null;

    // Redirect if no events left
    if (eventsGroupStore.currentGroup === null || 
        eventsGroupStore.currentGroup.events.length === 0) {
          router.push({ name: 'input' });
    }
  } catch (error) {
    console.error('Error deleting event:', error);
    ToastService.error(error.message || 'Failed to delete event');
  } finally {
    isLoading.value = false;
    loadingType.value = 'default';
  }
};

const handleExportAll = async () => {
  try {
    loadingType.value = 'export';
    isLoading.value = true;
    showExportConfirmation.value = false;
    
    // Create a delay between downloads to prevent browser issues
    for (const event of filteredEvents.value) {
      const filename = `${event.title.toLowerCase().replace(/\s+/g, '_')}.ics`;
      const downloadUrl = `${API_ENDPOINTS.events.downloadIcs(event.id)}`;
      
      await downloadFile(downloadUrl, filename);
      // Small delay between downloads
      await new Promise(resolve => setTimeout(resolve, 500));
    }
    
    ToastService.success('All events exported successfully');
  } catch (error) {
    console.error('Error exporting events:', error);
    ToastService.error('Failed to export events');
  } finally {
    isLoading.value = false;
    loadingType.value = 'default';
  }
};

const confirmExportAll = () => {
  const eventCount = filteredEvents.value.length;
  showExportConfirmation.value = true;
  exportConfirmationMessage.value = 
    `Are you sure you want to export ${eventCount} event${eventCount !== 1 ? 's' : ''}?`;
};

// Polling functions
const startPolling = () => {
  if (pollingInterval.value) return;
  
  pollingInterval.value = setInterval(async () => {
    try {
      if (!eventsGroupStore.processingStatus.complete) {
        await eventsGroupStore.fetchGroupDetails(route.params.id);
      }
      
      if (eventsGroupStore.processingStatus.complete || 
          eventsGroupStore.processingStatus.error) {
        stopPolling();
      }
    } catch (error) {
      console.error('Polling error:', error);
      stopPolling();
    }
  }, 2000);
};

const stopPolling = () => {
  if (pollingInterval.value) {
    clearInterval(pollingInterval.value);
    pollingInterval.value = null;
  }
};

// Fetch initial data
const fetchData = async () => {
  if (!route.params.id) return;
  
  try {
    await eventsGroupStore.fetchGroupDetails(route.params.id);
    
    if (!eventsGroupStore.processingStatus.complete && 
        !eventsGroupStore.processingStatus.error) {
      startPolling();
    }
  } catch (error) {
    console.error('Error fetching group details:', error);
    ToastService.error(error.message || 'Failed to load events');
  }
};

// Lifecycle hooks
onMounted(() => {
  fetchData();
});

onBeforeUnmount(() => {
  stopPolling();
  eventsGroupStore.clearCurrentGroup();
});
</script>

<template>
  <div class="min-h-screen bg-primary-50 dark:bg-primary-900 transition-colors duration-300">
    <!-- Header -->
    <HeaderActions
      :title="eventCountDisplay"
      :subtitle="eventsGroupStore.currentGroup ? 
                `Created ${new Date(eventsGroupStore.currentGroup.created_at).toLocaleDateString()}` : ''"
      :show-search="true"
      v-model:search-query="searchQuery"
      search-placeholder="Search events..."
      @back="handleBack"
    />

    <!-- Bulk Actions -->
    <BulkActions
      :disabled="isLoading || !filteredEvents.length"
      @calendar="handleAddAllToCalendar"
      @export="confirmExportAll"
      @delete="confirmBulkDelete"
    />

    <!-- Main Content -->
    <Transition
      enter-active-class="transition-all duration-500 ease-out"
      enter-from-class="opacity-0 translate-y-4"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition-all duration-300 ease-in"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 translate-y-4"
    >
      <main v-if="showContent" class="max-w-5xl mx-auto px-4 sm:px-6 py-3">
        <div class="grid gap-6">
          <TransitionGroup
            enter-active-class="transition-all duration-300 ease-out"
            enter-from-class="opacity-0 -translate-y-4"
            enter-to-class="opacity-100 translate-y-0"
            leave-active-class="transition-all duration-200 ease-in"
            leave-from-class="opacity-100 scale-100"
            leave-to-class="opacity-0 scale-95"
          >
            <div 
              v-for="event in filteredEvents" 
              :key="event.id"
            >
              <EventContent
                :event="event"
                @update="updates => handleEventUpdate(event.id, updates)"
                @export="() => handleAddToCalendar(event)"
                @share="() => {/* implement share */}"
                @download="() => {/* implement download */}"
                @delete="() => {confirmEventDelete(event.id)}"
              />
            </div>
          </TransitionGroup>
        </div>
      </main>
    </Transition>

    <!-- Error State -->
    <ErrorState
      v-if="eventsGroupStore.hasError"
      title="Error Loading Events"
      :message="eventsGroupStore.errorMessage"
    />

    <!-- Loading State -->
    <LoadingState
      :show="isLoading"
      :type="loadingType"
    />

    <!-- Delete Confirmation Dialog -->
    <ConfirmationDialog
      v-model:show="showBulkDeleteConfirmation"
      title="Delete All Events"
      message="Are you sure you want to delete all filtered events? This action cannot be undone."
      type="danger"
      confirm-label="Delete All"
      @confirm="handleBulkDelete"
      @cancel="showBulkDeleteConfirmation = false"
    />

    <ConfirmationDialog
      v-model:show="showSingleDeleteConfirmation"
      title="Delete Event"
      message="Are you sure you want to delete this event? This action cannot be undone."
      type="danger"
      confirm-label="Delete"
      @confirm="handleEventDelete"
      @cancel="showSingleDeleteConfirmation = false"
    />

    <ConfirmationDialog
      v-model:show="showExportConfirmation"
      title="Export All Events"
      :message="exportConfirmationMessage"
      confirm-label="Export"
      @confirm="handleExportAll"
      @cancel="showExportConfirmation = false"
    />
  </div>
</template>

<style scoped>
/* Custom scrollbar for desktop */
@media (min-width: 768px) {
  ::-webkit-scrollbar {
    width: 10px;
  }

  ::-webkit-scrollbar-track {
    @apply bg-neutral-100 dark:bg-primary-800;
  }

  ::-webkit-scrollbar-thumb {
    @apply bg-neutral-300 dark:bg-primary-600 rounded-full;
  }

  ::-webkit-scrollbar-thumb:hover {
    @apply bg-neutral-400 dark:bg-primary-500;
  }
}
</style>