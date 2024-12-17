<!-- views/LinkAccountView.vue -->
<script setup>
import { ref, computed } from 'vue';
import { 
  Link,
  ArrowLeft
} from 'lucide-vue-next';
import { Icon } from '@iconify/vue';
import CalendarProviderCard from '../components/calendar/CalendarProviderCard.vue';
import SyncStatus from '../components/calendar/SyncStatus.vue';
import { ToastService } from '../components/toast';

const isLoading = ref(true);
const providers = ref([
  {
    id: 'google',
    name: 'Google Calendar',
    icon: 'logos:google-calendar',
    description: 'Sync with your Google Calendar account',
    status: 'disconnected',
    bgColor: 'bg-white'
  },
  {
    id: 'apple',
    name: 'Apple Calendar',
    icon: 'bi:apple',  // Using Bootstrap Icons set for Apple
    description: 'Connect to your iCloud Calendar',
    status: 'connected',
    bgColor: 'bg-white'
  },
  {
    id: 'outlook',
    name: 'Outlook Calendar',
    icon: 'mdi:microsoft-outlook',
    description: 'Sync with your Microsoft Outlook account',
    status: 'error',
    error: 'Connection expired. Please reconnect your account.',
    bgColor: 'bg-white'
  }
]);

const connectedAccounts = computed(() => 
  providers.value.filter(p => p.status === 'connected').length
);

const handleLink = async (providerId) => {
  try {
    // Show loading toast
    ToastService.info(`Connecting to ${providerId} calendar...`);
    
    // Implementation would handle OAuth flow
    console.log('Linking account:', providerId);
    
    // Mock successful connection
    const provider = providers.value.find(p => p.id === providerId);
    if (provider) {
      provider.status = 'connected';
      provider.error = null;
      ToastService.success(`Successfully connected to ${provider.name}`);
    }
  } catch (error) {
    ToastService.error(`Failed to connect to ${providerId} calendar`);
    const provider = providers.value.find(p => p.id === providerId);
    if (provider) {
      provider.status = 'error';
      provider.error = error.message;
    }
  }
};

const handleUnlink = async (providerId) => {
  // Implementation would handle unlinking account
  console.log('Unlinking account:', providerId);
  
  // Mock successful disconnection
  const provider = providers.value.find(p => p.id === providerId);
  if (provider) {
    provider.status = 'disconnected';
  }
};

const handleDisconnect = async (providerId) => {
  try {
    ToastService.info(`Disconnecting ${providerId} calendar...`);
    
    const provider = providers.value.find(p => p.id === providerId);
    if (provider) {
      provider.status = 'disconnected';
      provider.error = null;
      ToastService.success(`Successfully disconnected from ${provider.name}`);
    }
  } catch (error) {
    ToastService.error(`Failed to disconnect from ${providerId} calendar`);
  }
};

const handleSync = async () => {
  // Implementation would trigger sync with all connected calendars
  console.log('Syncing calendars...');
  await new Promise(resolve => setTimeout(resolve, 1000));
};

// Simulate loading state
setTimeout(() => {
  isLoading.value = false;
}, 1000);
</script>

<template>
  <div class="min-h-screen bg-primary-50">
    <div class="max-w-5xl mx-auto px-4 py-8">
      <!-- Header -->
      <div class="flex items-center gap-4 mb-8">
        <router-link
          to="/"
          class="p-2 text-neutral-600 hover:text-accent-400 hover:bg-white rounded-lg transition-colors"
        >
          <ArrowLeft class="w-5 h-5" />
        </router-link>
        
        <div>
          <h1 class="text-2xl font-bold text-primary-500 flex items-center gap-2">
            <Link class="w-6 h-6" />
            Calendar Accounts
          </h1>
          <p class="text-neutral-600 mt-1">
            Connect and manage your calendar accounts
          </p>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="space-y-6">
        <div 
          v-for="i in 3" 
          :key="i"
          class="animate-pulse"
        >
          <div class="h-32 bg-white rounded-lg border border-neutral-200" />
        </div>
      </div>

      <!-- Content -->
      <div v-else class="space-y-6">
        <!-- Sync Status -->
        <SyncStatus
          last-sync="5 minutes ago"
          :connected-accounts="connectedAccounts"
          @sync="handleSync"
        />
        
        <!-- Calendar Providers -->
        <div class="space-y-4">
          <CalendarProviderCard
            v-for="provider in providers"
            :key="provider.id"
            :provider="provider"
            @link="handleLink"
            @unlink="handleUnlink"
          />
        </div>
      </div>
    </div>
  </div>
</template>