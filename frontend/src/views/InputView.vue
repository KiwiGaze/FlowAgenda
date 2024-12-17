<!-- views/InputView.vue -->
<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import MessageInput from '../components/MessageInput.vue';
import ShimmerLoader from '../components/ShimmerLoader.vue';
import { 
  Sparkles, 
  Calendar, 
  Users, 
  MapPin, 
  Zap,
  ArrowRight 
} from 'lucide-vue-next';
import { ToastService } from '../components/toast';
import { useEventsGroupStore } from '../stores/eventsGroupStore';

// Initialize store and router
const eventsGroupStore = useEventsGroupStore();
const router = useRouter();

// Local component states
const isLeaving = ref(false);
const showFeatures = ref(false);
const pollingInterval = ref(null);
const currentGroupId = ref(null);

// Polling functions
const startPolling = async (groupId) => {
  if (pollingInterval.value) return;
  
  pollingInterval.value = setInterval(async () => {
    try {
      await eventsGroupStore.fetchGroupDetails(groupId);
      
      // If processing is complete, navigate to the group view
      if (eventsGroupStore.processingStatus.complete) {
        stopPolling();
        await router.push({
          name: 'events-group',
          params: { id: groupId }
        });
      }
      
      // If there's an error, stop polling
      if (eventsGroupStore.processingStatus.error) {
        stopPolling();
        ToastService.error(eventsGroupStore.processingStatus.error);
      }
    } catch (error) {
      console.error('Polling error:', error);
      stopPolling();
    }
  }, 2000); // Poll every 2 seconds
};

const stopPolling = () => {
  if (pollingInterval.value) {
    clearInterval(pollingInterval.value);
    pollingInterval.value = null;
  }
};

// Handle form submission
const handleSubmit = async ({ text, useLLM }) => {
  try {
    if (!text?.trim()) {
      ToastService.error('Please enter event details');
      return;
    }

    isLeaving.value = true;
    eventsGroupStore.setProcessing(true);
    
    const result = await eventsGroupStore.createFromText(text, useLLM);
    
    if (!result?.group?.id) {
      throw new Error('Invalid response from server');
    }

    currentGroupId.value = result.group.id;
    
    // Start polling instead of immediate navigation
    if (!result.group.processing_complete) {
      startPolling(result.group.id);
    } else {
      // If already complete, navigate immediately
      await router.push({
        name: 'events-group',
        params: { id: result.group.id }
      });
    }

  } catch (error) {
    console.error('Error creating event:', error);
    isLeaving.value = false;
    eventsGroupStore.setProcessing(false);
    ToastService.error(
      error.message || 'Failed to process event. Please try again.'
    );
  }
};

onMounted(() => {
  // Animate features in after a short delay
  setTimeout(() => {
    showFeatures.value = true;
  }, 300);
});

// Cleanup on component unmount
onBeforeUnmount(() => {
  stopPolling();
  eventsGroupStore.clearCurrentGroup();
});
</script>

<template>
  <div class="min-h-screen bg-primary-50 dark:bg-primary-900 flex flex-col">
    <!-- Processing Overlay -->
    <Transition
      enter-active-class="transition-opacity duration-300"
      leave-active-class="transition-opacity duration-200"
      enter-from-class="opacity-0"
      leave-to-class="opacity-0"
    >
      <div v-if="eventsGroupStore.isProcessing" 
           class="fixed inset-0 bg-white/90 dark:bg-primary-900/90 backdrop-blur-sm z-50">
        <div class="max-w-2xl mx-auto px-4 py-12">
          <ShimmerLoader message="AI is processing your event..." />
        </div>
      </div>
    </Transition>

    <main class="flex-1 max-w-7xl mx-auto px-4 py-12 sm:py-16"
          :class="{ 'opacity-50': eventsGroupStore.isProcessing }">
      <div 
        class="w-full max-w-2xl mx-auto space-y-10 transition-all duration-300"
        :class="{ 'opacity-0 -translate-x-4': isLeaving }"
      >
        <!-- Header Section -->
        <div class="text-center space-y-6">
          <div 
            class="inline-flex items-center justify-center gap-2 bg-accent-50 dark:bg-accent-900/50 px-4 py-2 rounded-full 
                   transform hover:scale-105 transition-transform duration-200"
          >
            <Sparkles class="w-4 h-4 text-accent-400" />
            <span class="text-sm font-medium text-accent-500">AI-Powered Event Creation</span>
          </div>
          
          <h1 class="text-4xl font-bold text-primary-900 dark:text-primary-100 tracking-tight">
            Create Your Event
          </h1>
          
          <p class="text-lg text-neutral-600 dark:text-neutral-300 max-w-lg mx-auto">
            Describe your event in natural language and let our AI help you organize it perfectly.
          </p>
        </div>

        <!-- Input Section -->
        <MessageInput 
          :is-loading="eventsGroupStore.isLoading"
          @submit="handleSubmit"
          placeholder="Try 'Schedule a team meeting next Tuesday at 2 PM...'"
          :max-length="4000"
        >
          <template #helper>
            <div class="mt-4 text-center text-sm text-neutral-500 dark:text-neutral-400">
              Press Enter to create your event
            </div>
          </template>
        </MessageInput>
      </div>
    </main>
  </div>
</template>

<style scoped>
/* Smooth transitions */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* Card hover effects */
.hover-card {
  transition: all 0.2s ease-in-out;
}

.hover-card:hover {
  transform: translateY(-2px);
}
</style>