<!-- components/calendar/CalendarProviderCard.vue -->
<script setup>
import { ref } from 'vue';
import { 
  CheckCircle2, 
  XCircle,
  Loader2,
  ExternalLink,
  AlertCircle
} from 'lucide-vue-next';
import { Icon } from '@iconify/vue';

const props = defineProps({
  provider: {
    type: Object,
    required: true,
    // Shape: { id, name, icon, description, status, error }
  }
});

const emit = defineEmits(['link', 'unlink']);
const isLoading = ref(false);

const handleAction = async () => {
  if (isLoading.value) return;
  
  isLoading.value = true;
  try {
    if (props.provider.status === 'connected') {
      await emit('unlink', props.provider.id);
    } else {
      await emit('link', props.provider.id);
    }
  } finally {
    isLoading.value = false;
  }
};

const getStatusConfig = () => {
  switch (props.provider.status) {
    case 'connected':
      return {
        icon: CheckCircle2,
        iconClass: 'text-green-500',
        buttonText: 'Unlink Account',
        buttonClass: 'border-red-300 text-red-600 hover:bg-red-50'
      };
    case 'error':
      return {
        icon: AlertCircle,
        iconClass: 'text-red-500',
        buttonText: 'Retry Connection',
        buttonClass: 'border-accent-400 text-accent-400 hover:bg-accent-50'
      };
    default:
      return {
        icon: ExternalLink,
        iconClass: 'text-accent-400',
        buttonText: 'Connect Account',
        buttonClass: 'border-accent-400 text-accent-400 hover:bg-accent-50'
      };
  }
};
</script>

<template>
  <div 
    class="bg-white rounded-lg border border-neutral-200 overflow-hidden transition-all duration-200 hover:border-neutral-300"
  >
    <div class="p-6">
      <!-- Header -->
      <div class="flex items-start justify-between gap-4 text-left">
        <div class="flex items-center gap-4">
          <div 
            class="w-12 h-12 rounded-lg flex items-center justify-center"
            :class="provider.bgColor || 'bg-neutral-100'"
          >
            <Icon 
              :icon="provider.icon"
              class="w-8 h-8"
            />
          </div>
          
          <div>
            <h3 class="text-lg font-medium text-primary-500 mb-1">
              {{ provider.name }}
            </h3>
            <p class="text-sm text-neutral-600">
              {{ provider.description }}
            </p>
          </div>
        </div>

        <!-- Status Indicator -->
        <div class="flex items-center gap-2">
          <component 
            :is="getStatusConfig().icon"
            class="w-5 h-5"
            :class="getStatusConfig().iconClass"
          />
        </div>
      </div>

      <!-- Error Message -->
      <div 
        v-if="provider.error"
        class="mt-4 p-3 bg-red-50 text-red-600 text-sm rounded-lg"
      >
        {{ provider.error }}
      </div>

      <!-- Action Button -->
      <div class="mt-6 flex justify-end">
        <button
          @click="handleAction"
          class="px-4 py-2 rounded-lg border transition-all duration-200 flex items-center gap-2 disabled:opacity-50"
          :class="getStatusConfig().buttonClass"
          :disabled="isLoading"
        >
          <Loader2 
            v-if="isLoading"
            class="w-4 h-4 animate-spin"
          />
          <span>{{ getStatusConfig().buttonText }}</span>
        </button>
      </div>
    </div>
  </div>
</template>