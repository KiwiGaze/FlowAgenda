<!-- components/toast/ToastContainer.vue -->
<script setup>
import { TransitionGroup } from 'vue';
import ToastNotification from './ToastNotification.vue';

defineProps({
  toasts: {
    type: Array,
    required: true
  }
});

defineEmits(['close']);
</script>

<template>
  <div class="fixed top-4 right-4 z-50 flex flex-col gap-2 min-w-[320px] max-w-[420px]">
    <TransitionGroup
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="transform translate-x-full opacity-0"
      enter-to-class="transform translate-x-0 opacity-100"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="transform translate-x-0 opacity-100"
      leave-to-class="transform translate-x-full opacity-0"
    >
      <ToastNotification
        v-for="toast in toasts"
        :key="toast.id"
        v-bind="toast"
        @close="$emit('close', toast.id)"
      />
    </TransitionGroup>
  </div>
</template>