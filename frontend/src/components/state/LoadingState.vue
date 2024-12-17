<!-- components/state/LoadingState.vue -->
<script setup>
import { ref, computed } from 'vue';
// Add Export icon to imports
import { Loader2, Calendar, Download, Trash2, FileDown } from 'lucide-vue-next';

const props = defineProps({
  show: {
    type: Boolean,
    required: true
  },
  type: {
    type: String,
    default: 'default',
    // Add 'export' to valid types
    validator: (value) => ['default', 'calendar', 'download', 'delete', 'export'].includes(value)
  },
  message: {
    type: String,
    default: ''
  },
  blur: {
    type: Boolean,
    default: true
  }
});

// Add export configuration
const loadingConfig = {
  default: {
    icon: Loader2,
    defaultMessage: 'Loading...',
    iconClass: 'animate-spin',
    bgClass: 'bg-accent-50 dark:bg-accent-900/50'
  },
  calendar: {
    icon: Calendar,
    defaultMessage: 'Adding to calendar...',
    iconClass: 'animate-pulse',
    bgClass: 'bg-accent-50 dark:bg-accent-900/50'
  },
  download: {
    icon: Download,
    defaultMessage: 'Downloading...',
    iconClass: 'animate-pulse',
    bgClass: 'bg-accent-50 dark:bg-accent-900/50'
  },
  delete: {
    icon: Trash2,
    defaultMessage: 'Deleting...',
    iconClass: 'animate-bounce',
    bgClass: 'bg-red-50 dark:bg-red-900/50'
  },
  export: {
    icon: FileDown,
    defaultMessage: 'Exporting...',
    iconClass: 'animate-pulse',
    bgClass: 'bg-accent-50 dark:bg-accent-900/50'
  }
};

// Get current configuration based on type
const currentConfig = computed(() => loadingConfig[props.type]);

// Get display message - use prop message if provided, otherwise use default
const displayMessage = computed(() => props.message || currentConfig.value.defaultMessage);
</script>

<template>
  <Transition
    enter-active-class="transition-opacity duration-300"
    leave-active-class="transition-opacity duration-200"
    enter-from-class="opacity-0"
    leave-to-class="opacity-0"
  >
    <div 
      v-if="show"
      class="fixed inset-0 bg-black/20 dark:bg-black/40 flex items-center justify-center z-50"
      :class="{ 'backdrop-blur-sm': blur }"
    >
      <div 
        class="bg-white dark:bg-primary-800 rounded-lg p-6 shadow-xl 
               border border-neutral-200/50 dark:border-neutral-700/50
               flex items-center gap-4 transform hover:scale-102 transition-all
               duration-300 animate-fadeIn"
      >
        <div 
          class="p-2 rounded-full"
          :class="currentConfig.bgClass"
        >
          <component 
            :is="currentConfig.icon"
            class="w-6 h-6 text-accent-400"
            :class="currentConfig.iconClass"
          />
        </div>
        <span class="text-neutral-900 dark:text-neutral-100 font-medium">
          {{ displayMessage }}
        </span>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.animate-fadeIn {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>