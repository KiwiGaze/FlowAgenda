<!-- components/calendar/SyncStatus.vue -->
<script setup>
import { ref } from 'vue';
import { 
  RefreshCw,
  Check,
  Clock
} from 'lucide-vue-next';

const props = defineProps({
  lastSync: {
    type: String,
    required: true
  },
  connectedAccounts: {
    type: Number,
    required: true
  }
});

const emit = defineEmits(['sync']);
const isRefreshing = ref(false);

const handleSync = async () => {
  if (isRefreshing.value) return;
  
  isRefreshing.value = true;
  try {
    await emit('sync');
  } finally {
    setTimeout(() => {
      isRefreshing.value = false;
    }, 1000);
  }
};
</script>

<template>
  <div class="bg-white rounded-lg border border-neutral-200 p-6">
    <div class="flex items-center justify-between text-left">
      <div>
        <h2 class="text-lg font-medium text-primary-500 mb-2">
          Sync Status
        </h2>
        
        <div class="space-y-2">
          <!-- Connected Accounts -->
          <div class="flex items-center gap-2 text-sm text-neutral-600">
            <Check class="w-4 h-4 text-green-500" />
            <span>{{ connectedAccounts }} accounts connected</span>
          </div>
          
          <!-- Last Sync -->
          <div class="flex items-center gap-2 text-sm text-neutral-600">
            <Clock class="w-4 h-4" />
            <span>Last synced {{ lastSync }}</span>
          </div>
        </div>
      </div>

      <button
        @click="handleSync"
        class="p-2 text-accent-400 hover:bg-accent-50 rounded-lg transition-all duration-200 disabled:opacity-50"
        :disabled="isRefreshing"
      >
        <RefreshCw 
          class="w-5 h-5 transition-transform"
          :class="{ 'animate-spin': isRefreshing }"
        />
      </button>
    </div>
  </div>
</template>