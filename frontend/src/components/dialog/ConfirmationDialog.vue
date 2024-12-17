<!-- components/dialog/ConfirmationDialog.vue -->
<script setup>
import { computed } from 'vue';
import { AlertTriangle, AlertCircle, Info } from 'lucide-vue-next';

const props = defineProps({
  show: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    required: true
  },
  message: {
    type: String,
    required: true
  },
  type: {
    type: String,
    default: 'info',
    validator: (value) => ['info', 'warning', 'danger'].includes(value)
  },
  confirmLabel: {
    type: String,
    default: 'Confirm'
  },
  cancelLabel: {
    type: String,
    default: 'Cancel'
  }
});

const emit = defineEmits(['confirm', 'cancel']);

// Configuration for different dialog types
const dialogConfig = {
  info: {
    icon: Info,
    iconClass: 'text-accent-400',
    bgClass: 'bg-accent-50 dark:bg-accent-900/50',
    buttonClass: 'bg-accent-400 hover:bg-accent-500 focus:ring-accent-400/50'
  },
  warning: {
    icon: AlertCircle,
    iconClass: 'text-yellow-400',
    bgClass: 'bg-yellow-50 dark:bg-yellow-900/50',
    buttonClass: 'bg-yellow-400 hover:bg-yellow-500 focus:ring-yellow-400/50'
  },
  danger: {
    icon: AlertTriangle,
    iconClass: 'text-red-400',
    bgClass: 'bg-red-50 dark:bg-red-900/50',
    buttonClass: 'bg-red-500 hover:bg-red-600 focus:ring-red-500/50'
  }
};

// Get current configuration based on type
const currentConfig = computed(() => dialogConfig[props.type]);
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
      class="fixed inset-0 bg-black/20 dark:bg-black/40 backdrop-blur-sm 
             flex items-center justify-center z-50"
      @click.self="$emit('cancel')"
    >
      <div 
        class="w-full max-w-md bg-white dark:bg-primary-800 rounded-lg shadow-xl 
               border border-neutral-200/50 dark:border-neutral-700/50
               transform hover:scale-102 transition-transform p-6
               animate-fadeIn mx-4"
      >
        <!-- Header -->
        <div class="flex items-start gap-4">
          <div 
            class="p-2 rounded-full"
            :class="currentConfig.bgClass"
          >
            <component 
              :is="currentConfig.icon"
              class="w-6 h-6"
              :class="currentConfig.iconClass"
            />
          </div>
          <div class="flex-1 min-w-0">
            <h3 class="text-lg font-semibold text-neutral-900 dark:text-neutral-100">
              {{ title }}
            </h3>
            <p class="mt-2 text-neutral-600 dark:text-neutral-400">
              {{ message }}
            </p>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex justify-end gap-3 mt-6">
          <button
            @click="$emit('cancel')"
            class="px-4 py-2 text-sm font-medium text-neutral-700 dark:text-neutral-300
                   bg-neutral-100 dark:bg-neutral-700 rounded-lg
                   hover:bg-neutral-200 dark:hover:bg-neutral-600
                   focus:outline-none focus:ring-2 focus:ring-neutral-500/50
                   transition-all duration-200"
          >
            {{ cancelLabel }}
          </button>
          <button
            @click="$emit('confirm')"
            class="px-4 py-2 text-sm font-medium text-white rounded-lg
                   focus:outline-none focus:ring-2
                   transition-all duration-200"
            :class="currentConfig.buttonClass"
          >
            {{ confirmLabel }}
          </button>
        </div>
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