<!-- views/ResultsView.vue -->
<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { API_ENDPOINTS } from '../config/api';
import { ToastService } from '../components/toast';
import HeaderActions from '../components/actions/HeaderActions.vue';
import EventContent from '../components/EventContent.vue';
import LoadingState from '../components/state/LoadingState.vue';
import ErrorState from '../components/state/ErrorState.vue';
import ConfirmationDialog from '../components/dialog/ConfirmationDialog.vue';

const router = useRouter();
const route = useRoute();

// State
const event = ref(null);
const isLoading = ref(true);
const showActions = ref(true);
const isLeaving = ref(false);
const pollingInterval = ref(null);
const showDeleteConfirmation = ref(false);
const loadingType = ref('default');

// Poll event status
const pollEventStatus = async (eventId) => {
  try {
    const response = await fetch(API_ENDPOINTS.events.status(eventId), {
      headers: { 'Accept': 'application/json' }
    });
    
    if (!response.ok) throw new Error('Failed to fetch event status');

    const data = await response.json();
    if (!data.success) {
      throw new Error(data.error?.message || 'Failed to get event status');
    }

    if (data.data.processing_complete) {
      stopPolling();
      
      if (data.data.processing_error) {
        ToastService.error(data.data.processing_error);
        router.push({ name: 'input' });
        return;
      }
      
      event.value = data.data.event;
      isLoading.value = false;
      
      setTimeout(() => {
        showActions.value = true;
      }, 300);
    }
  } catch (error) {
    console.error('Error polling event status:', error);
    ToastService.error('Failed to get event updates');
    stopPolling();
    isLoading.value = false;
  }
};

const stopPolling = () => {
  if (pollingInterval.value) {
    clearInterval(pollingInterval.value);
    pollingInterval.value = null;
  }
};

// Event handlers
const handleBack = async () => {
  isLeaving.value = true;
  showActions.value = false;
  await new Promise(resolve => setTimeout(resolve, 150));
  router.back();
};

const handleEventUpdate = async (updates) => {
  try {
    const { field, value, isoDateTime } = updates;
    
    // Update local state
    if (event.value) {
      if (field.includes('start') || field.includes('end')) {
        const prefix = field.startsWith('start') ? 'start' : 'end';
        event.value[`${prefix}_datetime`] = isoDateTime;
      } else {
        event.value[field] = value;
      }
    }

    // Here you would make an API call to update the backend
    ToastService.success('Event updated successfully');
  } catch (error) {
    console.error('Error updating event:', error);
    ToastService.error('Failed to update event');
  }
};

const handleExport = async () => {
  try {
    loadingType.value = 'calendar';
    isLoading.value = true;
    
    // Add calendar export logic here
    await new Promise(resolve => setTimeout(resolve, 1000)); // Simulated delay
    
    ToastService.success('Event added to calendar successfully');
  } catch (error) {
    ToastService.error('Failed to add event to calendar');
  } finally {
    isLoading.value = false;
    loadingType.value = 'default';
  }
};

const handleShare = () => {
  ToastService.info('Copying share link...');
  // Add share implementation
  ToastService.success('Share link copied to clipboard');
};

const handleDownload = async () => {
  try {
    loadingType.value = 'download';
    isLoading.value = true;
    
    // Add download logic here
    await new Promise(resolve => setTimeout(resolve, 1000)); // Simulated delay
    
    ToastService.success('Event details downloaded');
  } catch (error) {
    ToastService.error('Failed to download event details');
  } finally {
    isLoading.value = false;
    loadingType.value = 'default';
  }
};

const confirmDelete = () => {
  showDeleteConfirmation.value = true;
};

const handleDelete = async () => {
  try {
    showDeleteConfirmation.value = false;
    loadingType.value = 'delete';
    isLoading.value = true;
    
    // Add delete logic here
    await new Promise(resolve => setTimeout(resolve, 1000)); // Simulated delay
    
    ToastService.success('Event deleted successfully');
    router.push({ name: 'input' });
  } catch (error) {
    ToastService.error('Failed to delete event');
    isLoading.value = false;
    loadingType.value = 'default';
  }
};

// Lifecycle hooks
onMounted(() => {
  const eventId = route.params.id;
  if (eventId) {
    pollingInterval.value = setInterval(() => pollEventStatus(eventId), 2000);
    pollEventStatus(eventId);
  } else {
    router.push({ name: 'input' });
  }
});

onUnmounted(() => {
  stopPolling();
});
</script>

<template>
  <div class="min-h-screen bg-primary-50 dark:bg-primary-900 transition-colors duration-300">
    <!-- Header -->
    <HeaderActions
      title="Event Details"
      :subtitle="event ? `Created ${new Date(event.created_at).toLocaleDateString()}` : ''"
      @back="handleBack"
    />

    <main class="max-w-5xl mx-auto px-4 sm:px-6 py-8 relative">
      <!-- Event Content -->
      <Transition
        enter-active-class="transition-all duration-500 ease-out"
        enter-from-class="opacity-0 translate-y-4"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition-all duration-300 ease-in"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 translate-y-4"
      >
        <div 
          v-if="event" 
          class="space-y-6"
          :class="{ 'opacity-0 translate-x-4': isLeaving }"
        >
          <EventContent
            :event="event"
            :show-actions="showActions"
            @update="handleEventUpdate"
            @export="handleExport"
            @share="handleShare"
            @download="handleDownload"
            @delete="confirmDelete"
          />
        </div>
      </Transition>

      <!-- Loading State -->
      <LoadingState 
        :show="isLoading"
        :type="loadingType"
      />

      <!-- Error State -->
      <ErrorState
        v-if="error"
        title="Error Loading Event"
        :message="error"
      />

      <!-- Delete Confirmation -->
      <ConfirmationDialog
        v-model:show="showDeleteConfirmation"
        title="Delete Event"
        message="Are you sure you want to delete this event? This action cannot be undone."
        type="danger"
        confirm-label="Delete"
        @confirm="handleDelete"
        @cancel="showDeleteConfirmation = false"
      />
    </main>
  </div>
</template>